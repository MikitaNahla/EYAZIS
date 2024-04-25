from nltk.corpus import wordnet


class WordsHandler:

    def __init__(self, words=None):
        self.words = words

    def findAllWordsForms(self):
        forms_of_words = []
        for word in self.words:
            forms_of_words.append(self.findForms(word))

        return forms_of_words

    def findForms(self, word):
        synonyms = self.findSynonyms(word)
        antonyms = self.findAntonyms(word)
        homonyms = self.findHomonyms(word)
        hyponyms = self.findHyponyms(word)
        hypernyms = self.findHypernyms(word)

        return {
            "synonyms": synonyms,
            "antonyms": antonyms,
            "homonyms": homonyms,
            "hyponyms": hyponyms,
            "hypernyms": hypernyms
        }

    @staticmethod
    def findSynonyms(word):
        synonyms = set()
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name())

        return list(synonyms)

    @staticmethod
    def findAntonyms(word):
        antonyms = set()
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                if lemma.antonyms():
                    antonyms.add(lemma.antonyms()[0].name())

        return list(antonyms)

    @staticmethod
    def findHomonyms(word):
        homonyms = set()

        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                homonyms.add(lemma.name())

        return list(homonyms)

    @staticmethod
    def findHyponyms(word):
        hyponyms = set()

        for syn in wordnet.synsets(word):
            for hyp in syn.hyponyms():
                for lemma in hyp.lemmas():
                    hyponyms.add(lemma.name())

        return list(hyponyms)

    @staticmethod
    def findHypernyms(word):
        hypernyms = set()

        for syn in wordnet.synsets(word):
            for hyp in syn.hypernyms():
                for lemma in hyp.lemmas():
                    hypernyms.add(lemma.name())

        return list(hypernyms)
