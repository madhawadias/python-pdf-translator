from services.google_translate import TranslationService
from google.api_core import exceptions
import google.auth.exceptions as google_auth_exceptions
import threading
# import swifter


class TranslateHelper:

    def __init__(self):
        try:
            self._translation_service = TranslationService()
        except google_auth_exceptions.GoogleAuthError:
            pass
        except exceptions.ClientError:
            pass

    def get_transaltion_client(self, df, index, input_column, output_column, row):
        input_cell = str(row[input_column])
        row[output_column] = self._translation_service.translate_text(input_cell)
        df.at[index, output_column] = row[output_column]

    def runner(self, df, input_column, results=[]):
        _output_column = 'translated'
        try:
            df[_output_column] = None
            count = 0
            _threads = []
            for index, row in df.iterrows():
                count = count + 1
                thread1 = threading.Thread(target=self.get_transaltion_client,
                                           args=(df, index, input_column, _output_column, row))
                _threads.append(thread1)
                thread1.start()
            for _thread in _threads:
                _thread.join()
            return df
        except Exception as e:
            return e
