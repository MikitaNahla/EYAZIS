from nltk import word_tokenize, pos_tag, ne_chunk

from imports import *
import matplotlib.pyplot as plt

if __name__ == "__main__":
    text = "The Bob see the Katy and he wants to talk to her, but he is too shy."

    tP = TextParser(text)
    sentences = tP.startParsing()

    sP = SentenceParser(sentences)
    sP.parseSentences()

    sentences = sP.getSentences()

    hJSON = HandleJSON('info/words.json')

    hJSON.readJSON()

    last_id = len(hJSON.getJSON()) | 0
    pT = ParseTree(sentences, last_id)
    pT.parseTrees()
    print(pT.getParseTrees())

    print(hJSON.getJSON())

    hJSON.setJSON(pT.getParseTrees())

    hJSON.writeJSON()
    print(hJSON.getJSON())

    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    plt.savefig('parse_tree.png', dpi=100)
