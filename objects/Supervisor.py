from states.Waiting import Waiting


class Supervisor():
    def __init__(self, obj):
        self.state = Waiting(self)
        self.strike = obj

    def update(self, field):
        self.state.update(field)