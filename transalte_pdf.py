import pdfplumber
from services.google_translate import TranslationService
from PyPDF2 import PdfFileReader
from googletrans import Translator
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph
from reportlab.platypus import SimpleDocTemplate
import pandas as pd
import os,time

# from translate_pdfs.fonts import *

"""
This script uses Google Translate library to translate the PDF
"""

"""
Constants
"""
URL_COM = 'translate.googleapis.com'
LANG = "en"

"""
FUNCTIONS
"""


# def get_translated_page_content(reader, lang):
#     """
#     Reads page content from the reader, translates it,
#     cleans it and returns page content as a list of strings.
#     Each entry in list represents a page
#     """
#     num_pages = reader.numPages
#     page_contents = []
#     translator = Translator(service_urls=[URL_COM])
#     for p in range(num_pages):
#         page = reader.getPage(p)
#         text = page.extractText()
#         print(text)
#         translation = translator.translate(text, dest=lang)
#         result_text = translation.text.replace("\n", " ").replace("W", "")
#         page_contents.append(result_text)
#     return page_contents

# def translate_pdf(path, lang):
#     file = open(path, 'rb')
#     reader = PdfFileReader(file)
#     page_contents = get_translated_page_content(reader, lang)
#
#     page_text = []
#     name = f'{LANG}_{path}'
#     pdf = SimpleDocTemplate(name, pagesize=letter)
#
#     for text in page_contents:
#         print(text)
#         page_text.append(
#             Paragraph(text, encoding='utf-8'))
#
#     pdf.build(page_text)

def get_translated_content(text, lang):
    text_list=text.split("\n")
    result_list=[]
    for item in text_list:
        if item==" ":
            print(item)
            result_list.append("\n")
        else:
            _translation_service = TranslationService()
            print(item)
            result_text = _translation_service.translate_text(item)
            print(result_text)
            result_text = result_text+"\n"
            result_list.append(result_text)
    result_text=''
    for text in result_list:
        result_text=result_text+text

    # translator = Translator(service_urls=[URL_COM])
    # print(text)
    # translation = translator.translate('विशेष रेनदे न', dest=lang, src='hi')
    # print(translation.src)
    result_text = result_text.replace("", "_").replace("\n", "<br />")
    return result_text


def extract_text(file_name):
    page_contents = []
    with pdfplumber.open(file_name) as pdf:
        pages = pdf.pages
        for i, pg in enumerate(pages):
            content = pages[i].extract_text()
            result_text = get_translated_content(text=content,lang=LANG)
            print(result_text)
            page_contents.append(result_text)

        # data = {'TEXT': page_contents}
        #
        # df = pd.DataFrame(data)
        # print(page_contents)
        # df.to_csv(r"urdu.csv", encoding='utf-8')
        page_text = []
        name = f'{LANG}_{file_name}'
        pdf = SimpleDocTemplate(name, pagesize=letter)

        for text in page_contents:
            print(text)
            page_text.append(
                Paragraph(text, encoding='utf-8'))

        pdf.build(page_text)


if __name__ == '__main__':
    file_name = "1608093540_702.pdf"
    # translate_pdf(file_name, LANG)
    extract_text(file_name=file_name)
