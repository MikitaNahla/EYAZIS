import json
from wordController import create_words, find_concordance, handle_concordance
import textDecoder
from textHandler import *
from nltk.stem import PorterStemmer, WordNetLemmatizer
from wordController import handle_file

if __name__ == "__main__":
    pdf_reader = textDecoder.PDFReader('input/test1.pdf')
    text = pdf_reader.get_information()
    lemmatizer = WordNetLemmatizer()
    stemmer = PorterStemmer()

    tH = TextHandler(text, 'en_core_web_sm', stemmer)
    # print(tH.load_text(), tH.find_all_lemmas('testing'), tH.find_stem('testing'))
    tH.convert_text_to_words()
    print(tH.start_handler())
    print(tH.find_all_lemmas('righteous'))
    b = 'The words. Another words'
    a = b.split(".")
    print(a, b)
    print(create_words('I like watching Tarantino\'s movies, my favourite are: Django and Kill Bill. I like go to the cinema. I think it\'s my favourite hobby. '))
    print(find_concordance('I love watching Tarantino\'s movies, my favourite are: Django and Kill Bill', {'word': 'love'}))
    # print(tH.find_all_lemmas('big'))
    # print(tH.words)
    # print(tH.get_info_by_ending_tag('NOUN', 'NNS'), tH.generate_word_by_rule('run', 'VERB'), tH.load_text())
    # print(tH.find_stem('running'), tH.start_handler())

