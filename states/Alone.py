from Logic import neighbours_in_radius
from states.Main import Main


class Alone(Main):
    def __init__(self, mob):
        Main.__init__(self, mob)
        self.communication = False

    def global_update(self, field):
        return self.mob.state.update(field)

    def global_check(self, field):
        nearest = neighbours_in_radius(self.mob.coord, 1, field)
        for each in nearest:
            if self.mob.stats.relationships[each.__class__.__name__] == "Attacking":
                self.communication = each
                return 2
            if self.mob.stats.relationships[each.__class__.__name__] == "Merging":
                self.communication = each
                return 3
        return self.mob.state.check(field)