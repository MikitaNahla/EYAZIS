import spacy
from lemminflect import getAllLemmas, getAllInflections, getAllInflectionsOOV
import re


class TextHandler:
    def __init__(self, text, lang, stemmer):
        self.text = text
        self.words = []
        self.nlp = spacy.load(lang)
        self.stemmer = stemmer
        self.designation_map = {
            'ADJ': {
                'JJ': 'Adjective',
                'JJR': 'Adjective, comparative',
                'JJS': 'Adjective, superlative'
            },
            'ADV': {
                'RB': 'Adverb',
                'RBR': 'Adverb, comparative',
                'RBS': 'Adverb, superlative'
            },
            'NOUN': {
                'NN': 'Noun, singular or mass',
                'NNS': 'Noun, plural'
            },
            'PROPN': {
                'NNP': 'Proper noun, singular or mass',
                'NNPS': 'Proper noun, plural'
            },
            'VERB': {
                'VB': 'Verb, base form',
                'VBD': 'Verb, past tense',
                'VBG': 'Verb, gerund or present participle',
                'VBN': 'Verb, past participle',
                'VBP': 'Verb, non-3rd person singular present',
                'VBZ': 'Verb, 3rd person singular present',
                'MD': 'Modal'
            }
        }

    def load_text(self):
        return self.nlp(self.text)

    def convert_text_to_words(self):
        self.words = self.text.split()

    def filter_punctuation_marks(self):
        original_words = []

        for word in self.words:
            if re.match(r'[A-Za-z]', word):
                original_words.append(word)

        self.words = original_words

    def filter_punctuation_in_words(self):
        for i, word in enumerate(self.words):
            self.words[i] = re.sub(r'[^A-Za-z]', '', word)

    def start_handler(self):
        self.filter_punctuation_marks()
        self.filter_punctuation_in_words()
        info = []
        for word in self.words:
            info_word = {}

            word_lemmas = self.find_all_lemmas(word)
            for key, word_lemma in word_lemmas.items():
                stem = self.find_stem(word_lemma[0].lower())
                if key == 'AUX':
                    key = 'VERB'
                part_of_speech = key
                endings = self.find_all_endings_and_info(word_lemma[0])

                info_word = {
                    'stem': stem,
                    'part_of_speech': part_of_speech,
                    'endings': endings,
                    }

            info.append({'word': word, 'info': info_word})

        return info

    @staticmethod
    def find_all_lemmas(word):
        return getAllLemmas(word)

    def find_stem(self, word):
        return self.stemmer.stem(word)

    def find_all_endings_and_info(self, word):
        inflections = getAllInflections(word)

        endings = set()
        for inflection, part_of_speech in inflections.items():
            form = part_of_speech[0]
            if form != word:
                endings.add((form.replace(word, ''), inflection))

        new_ending_info = []
        endings = list(endings)

        for ending in endings:
            part_of_speech = self.define_part_of_speech(ending[1])
            info = self.get_info_by_ending_tag(part_of_speech, ending[1])
            new_ending_info.append({"name": ending[0], "info": info})

        return new_ending_info

    def get_info_by_ending_tag(self, part_of_speech, tag):
        return self.designation_map[part_of_speech][tag]

    @staticmethod
    def define_part_of_speech(word_tag):
        if word_tag.startswith('N'):  # Существительное
            return 'NOUN'
        elif word_tag.startswith('P'):  # Имя собственное
            return 'PROPN'
        elif word_tag.startswith('V') or word_tag.startswith('AU'):  # Глагол или модальный глагол
            return 'VERB'
        elif word_tag.startswith('J'):  # Прилагательное
            return 'ADJ'
        elif word_tag.startswith('R'):
            return 'ADV'

    @staticmethod
    def generate_word_by_rule(word, part_of_speech):
        return getAllInflectionsOOV(word, part_of_speech)
