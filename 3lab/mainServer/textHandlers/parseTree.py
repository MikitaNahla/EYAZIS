import nltk
from nltk import Tree
from mainServer.textHandlers.wordsHandler import WordsHandler


class ParseTree:

    def __init__(self, sentence, sentence_id):
        self.sentence = sentence
        self.id = sentence_id
        self.grammar = r"""
                NP: {<DT|PP\$>?<JJ>*<NN>}   # Существительное с опциональными определителями и прилагательными
                {<NNP>+}                # Последовательность одного или более собственных существительных
                PP: {<IN><NP>}              # Предложная группа
                VP: {<VB.*><NP|PP|CLAUSE>+$}  # Глагол с последующими существительными, предложными группами или подчиненными предложениями
                CLAUSE: {<NP><VP>}          # Подчиненное предложение
            """
        self.parse_tree = None
        self.words_handler = WordsHandler()

    def parseSentence(self):
        self.parse_tree = {
            "id": self.id,
            "sentence": self.sentence.getSentence(),
            "parseTree": self.parseTree(self.sentence.entities, 0).get('tree')
        }

    def parseTree(self, entities, el_id):
        tree = []
        for entity in entities:
            if type(entity) == Tree:
                parseTree = self.parseTree(entity, el_id)
                tree.append({
                    "treeId": el_id,
                    "tree": parseTree.get('tree')
                })
                el_id = parseTree.get('el_id') + 1
            else:
                tree.append(
                    {
                        "wordId": el_id,
                        "word": entity[0],
                        "info": self.words_handler.findForms(entity[0]),
                        "role": entity[1]
                    }
                )
                el_id += 1

        return {"tree": tree, "el_id": el_id}

    def calculateTree(self):
        cp = nltk.RegexpParser(self.grammar)
        self.parse_tree = cp.parse(self.sentence.getTokens())

    def getParseTree(self):
        self.parseSentence()
        return self.parse_tree
