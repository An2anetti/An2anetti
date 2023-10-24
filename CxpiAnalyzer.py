from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, StringSetting

class CxpiAnalyzer(HighLevelAnalyzer):
    result_types = {
        'frame': {
            'format': '{{data}}',
            'name': 'Frame'
        }
    }

    CXPI_START = 0xC2
    CXPI_END = 0xC3
    THRESHOLD = 0.5  # Пороговое значение для определения "0" и "1" в долях времени

    def __init__(self):
        self.current_frame = []
        self.bit_length = 0

    def decode(self, frame):
        if len(frame) > 0:
            if frame[0] == self.CXPI_START:
                # Start of new frame
                self.current_frame = []

            self.current_frame.extend(frame)

            if frame[-1] == self.CXPI_END:
                # End of frame
                data = []

                for duration in self.current_frame:
                    bit = '1' if duration > self.bit_length * self.THRESHOLD else '0'
                    data.append(bit)

                data_str = ''.join(data)
                return AnalyzerFrame('frame', len(self.current_frame), {'data': data_str})

    def decode_data(self, data):
        frame = []

        for duration in data:
            frame.append(duration)

        return self.decode(frame)

    def decode_capture(self, capture, start, end):
        return self.decode_data(capture[start:end])

    def decode_capture_to_end(self, capture, start):
        return self.decode_data(capture[start:])

    def decode_capture_chunk(self, capture, start, end):
        return self.decode_data(capture[start:end])

    def settings(self):
        return []

    def generate_frames(self, data):
        return []

analyzer = CxpiAnalyzer()
