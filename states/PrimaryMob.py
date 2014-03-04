from states.Alone import Alone
from states.Finding import Finding


class PrimaryMob(Alone):
    def __init__(self, mob):
        Alone.__init__(self, mob)

    def update(self, field):
        self.mob.state = Finding(self.mob, [])
        return True

    def check(self, field):
        pass