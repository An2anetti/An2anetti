import asyncio
import serial

CXPI_START = 0xC2
CXPI_END = 0xC3
THRESHOLD = 0.5  # Пороговое значение для определения "0" и "1" в долях времени

async def read_serial_data():
    ser = serial.Serial('COM1', 9600)  # Замените 'COM1' на ваш порт и установите правильную скорость передачи данных

    current_frame = []
    bit_length = 0

    while True:
        data = ser.read(1)
        duration = int.from_bytes(data, 'big')  # Преобразование данных в число

        if duration == CXPI_START:
            # Start of new frame
            current_frame = []
        elif duration == CXPI_END:
            # End of frame
            data = []

            for duration in current_frame:
                bit = '1' if duration > bit_length * THRESHOLD else '0'
                data.append(bit)

            data_str = ''.join(data)
            print(data_str)

        current_frame.append(duration)

asyncio.run(read_serial_data())
