from states.Alone import Alone


class PrimaryProtagonist(Alone):
    def __init__(self, mob):
        Alone.__init__(self, mob)

    def update(self, field):
        from Logic import hex_visible_true
        hex_visible_true(field, self.mob.coord, self.mob.stats.view_radius)
        return True

    @staticmethod
    def check(field):
        return 6

