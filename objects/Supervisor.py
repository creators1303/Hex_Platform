class Supervisor():
    def __init__(self):
        from states.Waiting import Waiting
        self.state = Waiting(self)
        self.leads = []
        self.current_lead = 0

    def add_lead(self, lead):
        self.leads.append(lead)

    def update(self, field):
        return self.state.update(field)