from flask.views import MethodView
from abc import ABC, abstractmethod


class AbstractController(MethodView, ABC):

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def patch(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def put(self):
        pass

    @abstractmethod
    def post(self):
        pass
