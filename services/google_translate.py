from google.cloud import translate_v2 as translate
from google.oauth2 import service_account
import google.auth.exceptions as google_auth_exceptions
from google.api_core import exceptions
from langdetect import detect
import time


class TranslationService(object):
    def __init__(self):
        try:
            credentials = service_account.Credentials.from_service_account_file('C:/Users/ashen/Documents/kaliso/python-pdf-translator/credentials/test.json')
            self.translate_client = translate.Client(credentials=credentials)
        except google_auth_exceptions.GoogleAuthError:
            pass
        except exceptions.ClientError:
            pass

    def get_language(self, text):
        try:
            lang = detect(text)
            return lang
        except Exception as err:
            pass

    def translate_text(self, text):
        try:
            if text is not None:
                language = self.get_language(text)
                if language not in ["en", "und"]:
                    translation = self.translate_client.translate(text, target_language='EN')
                    return translation['translatedText']
                else:
                    return text
        except Exception as err:
            print(err)
            if str(err)[:3] == "403":
                try:
                    time.sleep(60)
                    translation = self.translate_client.translate(text, target_language='EN')
                    return translation['translatedText']
                except Exception as err:
                    pass
