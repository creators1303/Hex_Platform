from states.Alone import Alone


class PrimaryMob(Alone):
    def __init__(self, mob):
        Alone.__init__(self, mob)

    def update(self, field):
        return True

    def check(self, field):
        return 7