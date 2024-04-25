from mainServer.textHandlers.wordsHandler import WordsHandler

wH = WordsHandler(["good"])

forms = wH.findAllWordsForms()

print(forms)
