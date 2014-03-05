from pygame.time import get_ticks
from Logic import path_finding, hex_cube_to_offset, hex_visible_false, hex_visible_true, neighbours_in_radius
from states.Alone import Alone


class Walking(Alone):
    def __init__(self, mob, hexagon, field):
        Alone.__init__(self, mob)
        if hexagon != self.mob.coord:
            self.path = path_finding(self.mob.coord, hexagon, field, [])
        else:
            self.path = []
        self.step = get_ticks()

    def update(self, field):
        if self.path and get_ticks() - self.step >= self.mob.stats.step_time:
            hexagon = self.path[0]
            coord = hex_cube_to_offset(hexagon)
            if not field.map[coord[0]][coord[1]][1].passability:
                field.map[coord[0]][coord[1]][1].virtual_status_change(1)
            else:
                self.path = self.path[1:]
                hex_visible_false(field, self.mob.coord, self.mob.stats.view_radius)
                self.mob.going(field, hexagon)
                hex_visible_true(field, self.mob.coord, self.mob.stats.view_radius)
                self.step = get_ticks()
        return True

    def check(self, field):
        if not self.path:
            return 6
        nearest = neighbours_in_radius(self.mob.coord, 3, field)
        for each in nearest:
            if not self.mob.relationships_check(each) and self.mob.stats.relationships[each.__class__.__name__] == "Attacking":
                self.mob.add_info.append(each)
        return True
