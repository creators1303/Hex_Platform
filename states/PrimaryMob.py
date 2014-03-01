from states.Main import Main
from states.Finding import Finding


class PrimaryMob(Main):
    def __init__(self, mob):
        Main.__init__(self, mob)

    def update(self, field, size):
        self.mob.state = Finding(self.mob, [])
        return True

    def check(self, field):
        pass