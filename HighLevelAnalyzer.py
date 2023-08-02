from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, StringSetting

class CxpiAnalyzer(HighLevelAnalyzer):
    # Определение настроек анализатора
    my_string_setting = StringSetting(
    name='My String Setting',
    description='Enter a string:',
    default_value='Hello, World!'
)

    def __init__(self, settings):
        # Инициализация анализатора
        self.string_setting = self.my_string_setting
        super().__init__(settings=settings)

    def decode(self, frame: AnalyzerFrame):
        # Реализация метода decode() анализатора
        # Получение байта данных
        data = frame.data['data'][0]

        # Добавление кадра данных в вывод анализатора
        if len(frame.data['data']) > 1:
            # Кадр с битом четности
            parity = frame.data['data'][1]
            self.add_frame(
                frame=frame,
                start=frame.start_time,
                end=frame.end_time,
                data=data,
                parity=parity
            )
        else:
            # Кадр без бита четности
            self.add_frame(
                frame=frame,
                start=frame.start_time,
                end=frame.end_time,
                data=data
            )

    def get_value_string(self, frame: AnalyzerFrame):
        # Форматирование вывода анализатора
        if 'parity' in frame.data:
            return f'{frame.data["data"]}, P{frame.data["parity"]}'
        else:
            return f'{frame.data["data"]}'

analyzer = CxpiAnalyzer
