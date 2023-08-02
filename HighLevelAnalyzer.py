from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, StringSetting, NumberSetting, ChoicesSetting
from enum import Enum

class CxpiState(Enum):
    IDLE = 0
    DATA = 1

class CxpiAnalyzer(HighLevelAnalyzer):
    def __init__(self):
        self.current_state = CxpiState.IDLE
        self.current_byte = 0
        self.current_packet = []
        self.packet_start = False
        self.packet_end = False
        self.zero_count = 0
        self.last_packet = None
        self.packet_count = 0

    def decode(self, frame: AnalyzerFrame):
        if frame.type == 'result':
            if self.current_state == CxpiState.IDLE:
                if frame.data['data'] == 0:
                    self.current_state = CxpiState.DATA
                    self.current_byte = 0
                    self.current_packet = []
                    self.packet_start = True
                    self.packet_end = False
                    self.zero_count = 0
            elif self.current_state == CxpiState.DATA:
                if self.packet_start:
                    self.packet_start = False
                    self.zero_count = 0
                self.current_packet.append(frame.data['data'])
                self.current_byte += 1
                if self.current_byte == 8:
                    self.current_byte = 0
                    if len(self.current_packet) == 8:
                        byte_sum = sum(self.current_packet)
                        if byte_sum & 0xFF == 0xFF:
                            self.packet_end = True
                            self.last_packet = bytes(self.current_packet)
                            self.current_packet = []
                            self.current_state = CxpiState.IDLE
                            self.packet_count += 1
                        else:
                            self.current_state = CxpiState.IDLE
                    else:
                        self.current_state = CxpiState.IDLE
                else:
                    if frame.data['data'] == 0:
                        self.zero_count += 1
                    else:
                        self.zero_count = 0
                    if self.zero_count >= 3:
                        self.current_state = CxpiState.IDLE

        return None

    def get_available_channels(self):
        # Верните список доступных каналов, которые могут быть использованы анализатором
        return [0]

    def get_unique_id(self):
        # Верните уникальный идентификатор анализатора
        return "cxpi_analyzer"

    def get_name(self):
        # Верните имя анализатора
        return "CXPI Analyzer"

    def get_description(self):
        # Верните описание анализатора
        return "Анализатор CXPI"

    def get_config(self):
        # Верните конфигурацию анализатора
        return {
            'packet_size': NumberSetting(
                min_value=8,
                max_value=8,
                default_value=8,
                integer=True,
                label='Packet size',
                help='Size of each CXPI packet in bits'
            ),
            'packet_format': ChoicesSetting(
                default_value='sum',
                choices={
                    'sum': 'Sum of bytes',
                    'xor': 'XOR of bytes'
                },
                label='Packet format',
                help='Format used to check the packet checksum'
            )
        }

    def get_settings(self):
        # Верните настройки анализатора
        return {
            'packet_size': self.packet_size,
            'packet_format': self.packet_format
        }

    def set_settings(self, settings):
        # Примените изменения настроек анализатора
        self.packet_size = settings['packet_size']
        self.packet_format = settings['packet_format']

    def get_frames(self):
        # Верните список кадров, полученных анализатором
        frames = []
        if self.last_packet is not None:
            if self.packet_format == 'sum':
                packet_sum = sum(self.last_packet[:-1]) & 0xFF
                if packet_sum == self.last_packet[-1]:
                    frames.append(AnalyzerFrame(
                        'CXPI Packet',
                        self.last_packet,
                        self.last_packet[0] * 1000000,
                        (self.packet_size + 1) * 1000000
                    ))
            elif self.packet_format == 'xor':
                packet_xor = self.last_packet[0]
                for byte in self.last_packet[1:-1]:
                    packet_xor ^= byte
                if packet_xor == self.last_packet[-1]:
                    frames.append(AnalyzerFrame(
                        'CXPI Packet',
                        self.last_packet,
                        self.last_packet[0] * 1000000,
                        (self.packet_size + 1) * 1000000
                    ))
            self.last_packet = None

        return frames
