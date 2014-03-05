from states.Waiting import Waiting

class Supervisor():
    def __init__(self):
        self.state = Waiting(self)

    def update(self, field):
        self.state.update(field)