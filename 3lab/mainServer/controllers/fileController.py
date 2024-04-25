import json
from mainServer.controllers.abstractController import AbstractController
from mainServer.textHandlers.textDecoder import PDFReader
import os
from mainServer.app import UPLOAD_FOLDER, app
from flask import request, Blueprint
from mainServer.textHandlers.handleJSON import HandleJSON
from mainServer.textHandlers.sentenceParser import parseAllSentences
from mainServer.textHandlers.sentenceParser import SentenceParser

fileController = Blueprint('file', __name__)


class FileController(AbstractController):

    def post(self):
        file = request.files['file']

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        data = PDFReader(UPLOAD_FOLDER + file.filename)
        text = data.get_information().split('.')
        text.remove("  ")
        os.remove(file.filename)

        hJSON = HandleJSON('D:/Учёба/EYAZIS/3lab/mainServer/info/sentences.json')
        hJSON.readJSON()

        sP = SentenceParser(text)
        sP.parseSentences()

        lastSentenceId = 0

        sentences = sP.getSentences()
        if len(hJSON.getJSON()) != 0:
            lastSentenceId = hJSON.getJSON()[len(hJSON.getJSON()) - 1]["id"]

        parsed_sentences = parseAllSentences(sentences, lastSentenceId + 1)

        hJSON.appendJSON(parsed_sentences)
        hJSON.writeJSON()
        return json.dumps({'response': 'success'})

    def get(self):
        pass

    def patch(self):
        pass

    def delete(self):
        pass

    def put(self):
        pass


fileController.add_url_rule('/file/post', view_func=FileController.as_view('file'))
