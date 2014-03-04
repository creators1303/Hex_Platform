from Logic import hex_visible_true
from states.Alone import Alone
from states.Waiting import Waiting


class PrimaryPlayer(Alone):
    def __init__(self, mob):
        Alone.__init__(self, mob)

    def update(self, field):
        hex_visible_true(field, self.mob.coord, self.mob.stats.view_radius)
        self.mob.state = Waiting(self.mob)
        return True

    def check(self, field):
        pass

