from nltk import Tree


class ParseTree:

    def __init__(self, sentences):
        self.sentences = sentences
        self.parse_trees = []

    def parseTrees(self):
        for sentence in self.sentences:
            self.parse_trees.append(self.parseTree(sentence))

    def parseTree(self, sentence):
        tree = []
        for entity in sentence.entities:
            if type(entity) == Tree:
                tree.append({"tree": self.parseTree(entity)})
            else:
                tree.append({"word": entity[0], "role": entity[1]})
        return tree

    def getParseTrees(self):
        return self.parse_trees
