from st.Waiting import Waiting
from st.PrimarySupervisor import PrimarySupervisor


class Supervisor():
    def __init__(self):
        self.state = PrimarySupervisor(self)
        self.leads = []
        self.current_lead = 0

    def add_lead(self, lead):
        self.leads.append(lead)

    def state_update(self, field):
        status = self.state.update(field)
        if status == 5:
            self.state = Waiting(self)
        return status