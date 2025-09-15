  if(ev == tcpip_event) {
      // Nếu sự kiện là "có gói tin TCP/IP đến"
      tcpip_handler();   // Gọi hàm xử lý gói tin mạng
    }
    else if (ev == PROCESS_EVENT_TIMER) {
      // Nếu sự kiện là "hết thời gian timer"
      timeout_hanler();    // Gọi hàm xử lý khi timeout
      etimer_restart(&et); // Đặt lại timer (chu kỳ lặp)
    }
    else if (ev == sensors_event && data == &button_sensor) {
      // Nếu sự kiện đến từ cảm biến và cụ thể là nút bấm
      sensor_reading();   // Gọi hàm xử lý dữ liệu cảm biến
    }
  }

  PROCESS_END();   // Kết thúc tiến trình
}
