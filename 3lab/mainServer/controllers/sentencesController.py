import json
from mainServer.controllers.abstractController import AbstractController
from flask import Blueprint, request
from mainServer.textHandlers.handleJSON import HandleJSON
from mainServer.constants import NUM_EL_PER_PAGE

sentencesController = Blueprint('sentences', __name__)


class SentencesController(AbstractController):

    def post(self):
        pass

    def get(self, id=None, pageNumber=None):

        if id:
            hJSON = HandleJSON('D:/Учёба/EYAZIS/3lab/mainServer/info/sentences.json')
            hJSON.readJSON()
            dataJSON = hJSON.getJSON()
            tempSentence = ''
            for sentence in dataJSON:
                if sentence['id'] == id:
                    tempSentence = sentence

            return json.dumps(tempSentence)

        elif pageNumber:

            hJSON = HandleJSON('D:/Учёба/EYAZIS/3lab/mainServer/info/sentences.json')
            hJSON.readJSON()
            dataJSON = hJSON.getJSON()
            i = NUM_EL_PER_PAGE * (pageNumber - 1)
            last = i + NUM_EL_PER_PAGE
            if last < len(dataJSON):
                data = dataJSON[i:(i + NUM_EL_PER_PAGE)]
                tempPage = [
                    {
                        "id": record["id"],
                        "sentence": record["sentence"]
                    } for record in data
                ]
            else:
                data = dataJSON[i:]
                tempPage = [
                    {
                        "id": record["id"],
                        "sentence": record["sentence"]
                    } for record in data
                ]

            return json.dumps(tempPage)

    def patch(self, id=None):
        if id:
            hJSON = HandleJSON('D:/Учёба/EYAZIS/3lab/mainServer/info/sentences.json')
            hJSON.readJSON()
            dataJSON = hJSON.getJSON()
            inputData = request.json

            updateJSON(id, inputData, dataJSON)

            hJSON.setJSON(dataJSON)
            hJSON.writeJSON()

        return json.dumps({'response': 'success'})

    def delete(self):
        pass

    def put(self):
        pass


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
        if sentence[i]['wordId'] == inputData['wordId']:
            return i
        i += 1


sentencesController.add_url_rule(
    '/sentences/getPage/<int:pageNumber>',
    view_func=SentencesController.as_view('sentences'),
    methods=["GET"]
)
sentencesController.add_url_rule(
    '/sentences/get/<int:id>',
    view_func=SentencesController.as_view('get_sentence_by_id'),
    methods=["GET"]
)
sentencesController.add_url_rule(
    '/sentences/patch/<int:id>',
    view_func=SentencesController.as_view('sentences_patch_by_id'),
    methods=["PATCH"]
)
