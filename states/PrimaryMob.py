from states.Alone import Alone
from states.Pursuit import Pursuit


class PrimaryMob(Alone):
    def __init__(self, mob):
        Alone.__init__(self, mob)

    def update(self, field):
        self.mob.state = Pursuit(self.mob, [])
        return True

    @staticmethod
    def check(self, field):
        return True