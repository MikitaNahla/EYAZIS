from app import app
from mainServer.controllers.sentencesController import sentencesController
from mainServer.controllers.fileController import fileController
from mainServer.controllers.wordsController import wordsController

app.register_blueprint(sentencesController)
app.register_blueprint(fileController)
app.register_blueprint(wordsController)

if __name__ == "__main__":

    app.config["DEBUG"] = True
    app.run(debug=True)

