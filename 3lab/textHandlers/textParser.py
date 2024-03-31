import re


class TextParser:

    def __init__(self, text):
        self.text = text
        self.sentences = []

    def startParsing(self):
        self.parseText()
        return self.sentences

    def parseText(self):
        self.deleteNewRow()
        self.sentences = re.split(r'[.!?]+', self.text)
        self.deleteEmptySentences()
        self.deleteSpaces()

    def deleteEmptySentences(self):
        for sentence in self.sentences:
            if sentence == '':
                self.sentences.remove('')

    def deleteSpaces(self):
        new_sentences = []
        for sentence in self.sentences:
            new_sentences.append(self.prepareSentence(sentence))

        self.sentences = new_sentences

    @staticmethod
    def prepareSentence(sentence):
        sentence = sentence.split(' ')
        for word in sentence:
            if word == '':
                sentence.remove('')

        return ' '.join(sentence)

    def deleteNewRow(self):
        self.text = re.sub(r'\n', '', self.text)

