from imports import *

if __name__ == "__main__":
    text = """At eight o'clock on Thursday morning.
     The cat sees the dog, but dog doesn't see the cat, so we don't make a noise."""

    tP = TextParser(text)
    sentences = tP.startParsing()

    sP = SentenceParser(sentences)
    sP.parseSentences()

    sentences = sP.getSentences()

    pT = ParseTree(sentences)
    pT.parseTrees()
    print(pT.getParseTrees())
