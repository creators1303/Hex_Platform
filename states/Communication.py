from states.Main import Main


class Communication(Main):
    def __init__(self, mob, strike):
        Main.__init__(self, mob)
        self.communication = strike

    def global_update(self, field):
        return self.mob.current_state.update(field)

    def global_check(self, field):
        from Logic import hex_distance, hex_visible_true
        if self.mob.stats.view_radius:
            hex_visible_true(field, self.mob.coord, self.mob.stats.view_radius)
        if self.communication.health <= 0 or hex_distance(self.mob.coord, self.communication.coord) > 1:
            return 9
        return self.mob.current_state.check(field)