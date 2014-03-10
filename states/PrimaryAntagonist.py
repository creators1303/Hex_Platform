from states.Alone import Alone


class PrimaryAntagonist(Alone):
    def __init__(self, mob):
        Alone.__init__(self, mob)

    @staticmethod
    def update(field):
        return True

    @staticmethod
    def check(field):
        return 7