from saleae.data import *
from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, StringSetting, NumberSetting, ChoicesSetting

class CxpiAnalyzer(HighLevelAnalyzer):
    # Определение настроек анализатора
    my_string_setting = StringSetting(
        name='My String Setting',
        description='Enter a string:',
        default_value='Hello, World!'
    )
    my_number_setting = NumberSetting(
        name='My Number Setting',
        description='Enter a number:',
        min_value=0,
        max_value=100,
        default_value=50
    )
    my_choices_setting = ChoicesSetting(
        name='My Choices Setting',
        description='Choose an option:',
        choices=('Option 1', 'Option 2', 'Option 3'),
        default_value='Option 1'
    )

    def decode(self, frame: AnalyzerFrame):
        # Получаем данные из текущего фрейма
        data = frame.data['data']

        # Разбираем данные пакета протокола CXPI
        # и получаем необходимые для анализа параметры
        # ...

        # Создаем объект AnalyzerFrame с результатами анализа
        result_data = {} # Определение переменной result_data
        result_frame = AnalyzerFrame(
            'CXPI', 
            frame.start_time, 
            frame.end_time, 
            {'result_data_key': result_data},
            metadata=None,
            attachments=None
        )

        # Возвращаем результат анализа
        return result_frame
