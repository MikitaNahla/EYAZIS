import json
from mainServer.controllers.abstractController import AbstractController
from flask import Blueprint, request
from mainServer.textHandlers.handleJSON import HandleJSON

wordsController = Blueprint('words', __name__)


class WordsController(AbstractController):

    def get(self, id=None):
        hJSON = HandleJSON('D:/Учёба/EYAZIS/3lab/mainServer/info/sentences.json')
        hJSON.readJSON()
        dataJSON = hJSON.getJSON()

        wordInfo = request.json

        tempSentence = findSentence(id, dataJSON)
        tempWord = findWord(tempSentence, wordInfo)

        return json.dumps(tempWord)

    def patch(self):
        pass

    def post(self):
        pass

    def put(self, id=None):
        if id:
            hJSON = HandleJSON('D:/Учёба/EYAZIS/3lab/mainServer/info/sentences.json')
            hJSON.readJSON()
            dataJSON = hJSON.getJSON()
            wordInfo = request.json

            updateJSON(id, wordInfo, dataJSON)

            hJSON.setJSON(dataJSON)
            hJSON.writeJSON()

        return json.dumps({"response": "success"})

    def delete(self):
        pass


def findSentence(sentenceId, data):
    for sentence in data:
        if sentence['id'] == sentenceId:
            return sentence


def findWord(sentence, wordInfo):
    for word in sentence['parseTree']:
        if json.dumps(wordInfo) == json.dumps(word):
            return word


def updateJSON(sentenceId, inputData, dataJSON):
    for sentence in dataJSON:
        if sentence['id'] == sentenceId:
            index = findIndex(inputData, sentence['parseTree'])
            for key in inputData:
                sentence['parseTree'][index][key] = inputData[key]
            return


def findIndex(inputData, sentence):
    i = 0
    while i < len(sentence):
        if 'wordId' in inputData:
            if sentence[i]['wordId'] == inputData['wordId']:
                return i
        elif 'treeId' in inputData:
            if sentence[i]['treeId'] == inputData['treeId']:
                return i
        i += 1


wordsController.add_url_rule(
    '/words/get/<int:id>',
    view_func=WordsController.as_view('get_info_by_id'),
    methods=["GET"]
)
wordsController.add_url_rule(
    '/words/put/<int:id>',
    view_func=WordsController.as_view('word_put_by_id'),
    methods=["PUT"]
)
