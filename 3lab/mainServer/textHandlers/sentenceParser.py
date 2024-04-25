import nltk
from mainServer.textHandlers.parseTree import ParseTree


class SentenceParser:
    def __init__(self, sentences):
        self.sentences = sentences

    def parseSentences(self):
        parsed_sentences = []
        for sentence in self.sentences:
            new_sentence = Sentence(sentence)
            self.fillFields(new_sentence, sentence)
            parsed_sentences.append(new_sentence)

        self.sentences = parsed_sentences

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

    def getTokens(self):
        return self.tokens

    def getSentence(self):
        return self.sentence

    def getEntities(self):
        return self.entities

    def print(self):
        print(self.sentence)


def parseAllSentences(sentences, lastSentenceId):
    parsed_sentences = []
    for sentence in sentences:
        pT = ParseTree(sentence, lastSentenceId)
        parsed_sentences.append(pT.getParseTree())
        lastSentenceId += 1
    return parsed_sentences

