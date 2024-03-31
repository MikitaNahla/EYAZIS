import nltk
import lemminflect

from nltk import pos_tag
from nltk.tokenize import word_tokenize

from nltk.corpus import wordnet

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('tagsets')


class TextHandler:
    def __init__(self, text, lemmatizer, stemmer):
        self.text = text
        self.tokens = []
        self.words = []
        self.lemmatizer = lemmatizer
        self.stemmer = stemmer
        self.pos_map = {
            'CC': 'coordinating conjunction',
            'CD': 'cardinal digit',
            'DT': 'determiner',
            'EX': 'existential there (like: "there is" ... think of it like "there exists")',
            'FW': 'foreign word',
            'IN': 'preposition/subordinating conjunction',
            'JJ': 'adjective',
            'JJR': 'adjective, comparative',
            'JJS': 'adjective, superlative',
            'LS': 'list marker',
            'MD': 'modal',
            'NN': 'noun, singular',
            'NNS': 'noun plural',
            'NNP': 'proper noun, singular',
            'NNPS': 'proper noun, plural',
            'PDT': 'predeterminer',
            'POS': 'possessive ending',
            'PRP': 'personal pronoun',
            'PRP$': 'possessive pronoun',
            'RB': 'adverb',
            'RBR': 'adverb, comparative',
            'RBS': 'adverb, superlative',
            'RP': 'particle',
            'TO': 'to',
            'UH': 'interjection',
            'VB': 'verb, base form',
            'VBD': 'verb, past tense',
            'VBG': 'verb, gerund/present participle',
            'VBN': 'verb, past participle',
            'VBP': 'verb, sing. present, non-3d',
            'VBZ': 'verb, 3rd person sing. present',
            'WDT': 'wh-determiner',
            'WP': 'wh-pronoun',
            'WP$': 'possessive wh-pronoun',
            'WRB': 'wh-abverb'
        }

    # Найти основу слова

    def stemmize(self, word):
        return self.stemmer.stem(word)

    # Выделяем токены текста
    def tokenize_text(self):
        self.tokens = word_tokenize(self.text, language='english')
        # print(tokens)

    # Определяем часть речи
    @staticmethod
    def define_part_of_speech(word):
        return pos_tag([word])

    # Найти начальную форму слова

    def word_base_handler(self, word):
        word_tag = self.define_speech_tag(self.define_part_of_speech(word))
        lemma = self.lemmatizer.lemmatize(word, pos=word_tag)
        print(lemma)
        return lemma

    # Определить тег слова части речи

    @staticmethod
    def define_speech_tag(tag):
        word_tag = tag[0][1]
        if word_tag.startswith('N'):  # Существительное
            return 'n'
        elif word_tag.startswith('V'):  # Глагол
            return 'v'
        elif word_tag.startswith('J'):  # Прилагательное
            return 'a'
        elif word_tag.startswith('R'):  # Наречие
            return 'r'

    # Определение окончания

    @staticmethod
    def define_ending(word, stem):
        return word[len(stem):]

    # Определение информации о части речи

    def define_speech_info(self, word_tag):
        return self.pos_map[word_tag]

    # Найти форму слова

    @staticmethod
    def find_word_form(word):
        return
