from Logic import neighbours_in_radius
from states.Main import Main


class Communication(Main):
    def __init__(self, mob):
        Main.__init__(self, mob)

    def global_update(self, field):
        nearest = neighbours_in_radius(self.mob.coord, 1, field)
        for each in nearest:
            if self.mob.stats.relationships[each.__class__.__name__] == "Attacking":
                return 2
        self.mob.state.update(field)