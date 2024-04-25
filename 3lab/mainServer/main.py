from imports import *

if __name__ == "__main__":
    text = "This is a sample sentence."

    tP = TextParser(text)
    sentences = tP.startParsing()

    sP = SentenceParser(sentences)
    sP.parseSentences()

    sentences = sP.getSentences()

    hJSON = HandleJSON('info/sentences.json')

    hJSON.readJSON()

    last_id = len(hJSON.getJSON()) | 0

    st = parseAllSentences(sentences)

