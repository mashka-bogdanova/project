from googletrans import Translator
from transliterate import translit

def translation(title):
    translator = Translator()
    str = "'" + title + "'"
    title_ru = translator.translate(str, dest='ru').text
    return title_ru

print(translation('The Shining'))
