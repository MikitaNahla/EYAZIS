import json


class HandleJSON:

    def __init__(self, filename):
        self.filename = filename
        self.data = []

    def getJSON(self):
        return self.data

    def setJSON(self, data):
        self.data = data

    def appendJSON(self, new_sentences):
        for sentence in new_sentences:
            self.data.append(sentence)

    def readJSON(self) -> None:
        with open(self.filename, 'r') as file:
            self.data = json.load(file)

    def writeJSON(self):
        with open(self.filename, 'w') as file:
            json.dump(self.data, file, indent=4)
