from .Facade import Facade

class Controller():
    facade: Facade = None

    def __init__(self):
        self.facade = Facade()

    def run(self):
        self.facade.run()