class Supervisor():
    def __init__(self, obj):
        from states.Waiting import Waiting
        self.state = Waiting(self)
        self.strike = obj

    def update(self, field):
        self.state.update(field)