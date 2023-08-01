from saleae.data import *
from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, StringSetting, NumberSetting, ChoicesSetting

class CxpiAnalyzer(HighLevelAnalyzer):
    def decode(self, frame: AnalyzerFrame):
        # Получаем данные из текущего фрейма
        data = frame.data['data']


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