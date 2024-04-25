import nltk
nltk.download('maxent_ne_chunker')
nltk.download('words')


class SentenceParser:
    def __init__(self, sentences):
        self.sentences = sentences

    def parseSentences(self):
        new_sentences = []
        for sentence in self.sentences:
            new_sentence = Sentence(sentence)
            self.fillFields(new_sentence, sentence)
            new_sentences.append(new_sentence)

        self.sentences = new_sentences

    def fillFields(self, new_sentence, sentence):
        new_sentence.tokens = self.tokenizeWords(sentence)
        new_sentence.tags = self.tagWords(new_sentence)
        new_sentence.entities = self.identifyEntities(new_sentence)

    @staticmethod
    def tokenizeWords(sentence):
        return nltk.word_tokenize(sentence)

    @staticmethod
    def tagWords(sentence):
        return nltk.pos_tag(sentence.tokens)

    @staticmethod
    def identifyEntities(sentence):
        return nltk.chunk.ne_chunk(sentence.tags)

    def getSentences(self):
        return self.sentences


class Sentence:
    def __init__(self, sentence):
        self.sentence = sentence
        self.tokens = []
        self.tags = []
        self.entities = []

    def getSentence(self):
        return self.sentence

    def print(self):
        print(self.sentence)
