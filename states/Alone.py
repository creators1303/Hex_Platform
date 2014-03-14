from states.Main import Main


class Alone(Main):
    def __init__(self, mob):
        Main.__init__(self, mob)
        self.communication = False
        self.avoid = []

    def global_update(self, field):
        return self.mob.current_state.update(field)

    def global_check(self, field):
        from Logic import neighbours_in_radius
        if self.mob.stats.view_radius:
            from Logic import hex_visible_true
            hex_visible_true(field, self.mob.coord, self.mob.stats.view_radius)

        nearest = neighbours_in_radius(self.mob.coord, 1, field)
        for each in nearest:
            if self.mob.stats.relationships[each.__class__.__name__] == "Attacking":
                self.communication = each
                return 2
            if self.mob.stats.relationships[each.__class__.__name__] == "Merging":
                self.communication = each
                return 3
        nearest = neighbours_in_radius(self.mob.coord, 3, field)
        for each in nearest:
            if not self.mob.relationships_check(each) and self.mob.stats.relationships[
                each.__class__.__name__] == "Attacking" and not each in self.avoid:
                self.avoid.append(each)
        for each in self.avoid:
            if each.health <= 0:
                self.avoid.remove(each)
        return self.mob.current_state.check(field)