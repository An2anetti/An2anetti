from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, StringSettingOption

class CxpiAnalyzer(HighLevelAnalyzer):
    # Определение настроек анализатора
    my_string_setting = StringSettingOption(
        id='my_string_setting',
        name='My String Setting',
        description='Enter a string:',
        default_value='Hello, World!'
    )

    def __init__(self):
        # Инициализация анализатора
        self.string_setting = self.my_string_setting

    def decode(self, frame: AnalyzerFrame):
        # Получаем данные из текущего фрейма
        data = frame.data['data']

        # Проверяем длину пакета
        if len(data) < 2:
            # Пакет не полный, пропускаем его
            return None

        # Проверяем, что первый байт соответствует стартовому байту протокола CXPI
        if data[0] != 0x80:
            # Пакет не соответствует протоколу CXPI, пропускаем его
            return None

        # Извлекаем данные из пакета
        data_length = data[1]
        message_id = data[2]
        message_data = data[3:3+data_length]

        # Создаем объект AnalyzerFrame с результатами анализа
        result_data = {
            'data_length': data_length,
            'message_id': message_id,
            'message_data': message_data
        }
        result_frame = AnalyzerFrame(
            'CXPI', 
            frame.start_time, 
            frame.end_time, 
            result_data,
            metadata=None,
            attachments=None
        )

        # Возвращаем результат анализа
        return result_frame
