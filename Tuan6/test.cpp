uint32_t tickstart = HAL_GetTick();
uint32_t wait = Delay;

if (wait < HAL_MAX_DELAY) {
  wait += (uint32_t)(uwTickFreq);
}

while ((HAL_GetTick() - tickstart) < wait);
