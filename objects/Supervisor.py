class Supervisor():
    def __init__(self):
        from states.PrimarySupervisor import PrimarySupervisor
        self.state = PrimarySupervisor(self)
        self.leads = []
        self.current_lead = 0

    def add_lead(self, lead):
        self.leads.append(lead)

    def state_update(self, field):
        status = self.state.update(field)
        if status == 5:
            from states.Waiting import Waiting
            self.state = Waiting(self)
        return status