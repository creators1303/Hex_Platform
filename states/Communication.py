from Logic import hex_distance
from states.Main import Main


class Communication(Main):
    def __init__(self, mob):
        Main.__init__(self, mob)
        self.communication = False

    def global_update(self, field):
        return self.mob.current_state.update(field)

    def global_check(self, field):
        if self.communication.health <= 0 or hex_distance(self.mob.coord, self.communication.coord) > 1:
            return 9
        return self.mob.current_state.check(field)