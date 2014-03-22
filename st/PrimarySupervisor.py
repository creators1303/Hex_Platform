from st.Alone import Alone


class PrimarySupervisor(Alone):
    def __init__(self, mob):
        Alone.__init__(self, mob)

    def update(self, field):
        field.camera.set_lead(self.mob.leads[self.mob.current_lead])
        return 5