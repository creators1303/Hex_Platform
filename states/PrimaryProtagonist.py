from Logic import hex_visible_true
from states.Alone import Alone


class PrimaryProtagonist(Alone):
    def __init__(self, mob):
        Alone.__init__(self, mob)

    def update(self, field):
        hex_visible_true(field, self.mob.coord, self.mob.stats.view_radius)
        return True

    @staticmethod
    def check(field):
        return 6

