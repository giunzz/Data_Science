/*
 * feeding.c
 *
 *  Created on: Sep 15, 2025
 *      Author: NHU Y
 */
#include "feeding.h"

struct feeding_t *_feed;

DS3231_Time_t settime = {
		.seconds = 0,
		.minutes = 16,
		.hour = 15,
		.dayofweek = 5,
		.dayofmonth = 25,
		.month = 9,
		.year = 25
};

static void feeding_Servo_Angle(int16_t angle);

void feeding_ISR(uint16_t GPIO_Pin) {
	if (GPIO_Pin == Button_Pin) {
		if(_feed->IsSetTime == 0)
			_feed->IsFeed = 1;
		else
			_feed->IsSetTime = 2;
	}
	if (GPIO_Pin == Alarm_Pin) {
		uint8_t status;
		HAL_I2C_Mem_Read(_feed->hi2c, 0xD0, 0x0F, 1, &status, 1, 1000);
		status &= ~(1<<0);
		HAL_I2C_Mem_Write(_feed->hi2c, 0xD0, 0x0F, 1, &status, 1, 1000);
		HAL_GPIO_TogglePin(LED_GPIO_Port, LED_Pin);
		_feed->IsFeed = 1;
	}
	if (GPIO_Pin == Button_Up_Pin) {
		_feed->IsSetTime = 1;
		_feed->alarm_time.hour++;
		if (_feed->alarm_time.hour >= 24) _feed->alarm_time.hour = 0;
//		_feed->alarm_time.minutes++;
//		if (_feed->alarm_time.minutes >= 60) _feed->alarm_time.minutes = 0;
	}
	if (GPIO_Pin == Button_Dw_Pin) {
		_feed->IsSetTime = 1;
		_feed->alarm_time.hour--;
		if (_feed->alarm_time.hour < 0) _feed->alarm_time.hour = 23;
//		_feed->alarm_time.minutes--;
//		if (_feed->alarm_time.minutes < 0) _feed->alarm_time.minutes = 59;
	}
}

void feeding_Servo_Spin(uint32_t delay_time) {
    switch(_feed->IsFeed) {
        case 1:
            feeding_Servo_Angle(180);
            _feed->IsFeed = 2;
            break;
        case 3:
            feeding_Servo_Angle(0);
    		_feed->IsFeed = 0;
        	break;
    }
}

void feeding_Handler(void) {
	if (_feed->IsFeed != 0){
		feeding_Servo_Spin(1000);
	}
	if (_feed->IsSetTime == 2){
		// Send feed schedule alarm
		DS3231_SetAlarm(_feed->alarm_time);
		_feed->IsSetTime = 0;
	}
}

void feeding_Init(struct feeding_t *feed) {
	_feed = feed;
	DS3231_Init(_feed->hi2c);
	HAL_TIM_PWM_Start(_feed->htim, _feed->channel);
	feeding_Servo_Angle(0);
//	DS3231_SetTime(settime);
}

static void feeding_Servo_Angle(int16_t angle) {
	if(angle > 180) angle = 180;
	if(angle < 0) angle = 0;

	int duty = -(angle * 50/9) + 1250;
	__HAL_TIM_SET_COMPARE(_feed->htim, _feed->channel, duty);
	_feed->angle = angle;
}

/* Unused */
//uint8_t feeding_delay(uint32_t delay_ms) {
//    static uint32_t tickstart = 0;
//    static uint8_t active = 0;
//
//    if (!active) {
//        tickstart = HAL_GetTick();
//        active = 1;
//        return 0;
//    }
//
//    if ((HAL_GetTick() - tickstart) >= delay_ms) {
//        active = 0;
//        return 1;
//    }
//    return 0;
//}
//void feeding_Servo_Spin(uint32_t delay_time) {
//    static uint8_t state = 0;
//    static uint32_t tickstart = 0;
//
//    switch(state) {
//        case 0:
//            feeding_Servo_Angle(180);
//            tickstart = HAL_GetTick();
//            state = 1;
//            break;
//
//        case 1:
//            if (HAL_GetTick() - tickstart >= delay_time) {
//                feeding_Servo_Angle(0);
//                state = 0;
//        		_feed->IsFeed = 0;
//            }
//            break;
//    }
//}
