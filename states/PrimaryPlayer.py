from Logic import hex_visible_true
from states.Main import Main
from states.Waiting import Waiting


class PrimaryPlayer(Main):
    def __init__(self, mob):
        Main.__init__(self, mob)

    def update(self, field, size):
        hex_visible_true(field, self.mob.coord, self.mob.stats.view_radius)
        self.mob.state = Waiting(self.mob)
        return True

    def check(self, field):
        pass

