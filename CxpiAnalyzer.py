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

    def __init__(self):
        self.current_frame = []

    def decode(self, frame):
        if len(frame) > 0:
            if frame[0] == self.CXPI_START:
                # Start of new frame
                self.current_frame = []

            self.current_frame.extend(frame)

            if frame[-1] == self.CXPI_END:
                # End of frame
                data = ''.join('{:02X}'.format(byte) for byte in self.current_frame)
                return AnalyzerFrame('frame', len(self.current_frame), {'data': data})

    def decode_data(self, data):
        frame = []

        for byte in data:
            frame.append(ord(byte))

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
