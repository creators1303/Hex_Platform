from pygame.time import get_ticks
from states.Alone import Alone
from Logic import unexplored_finding, hex_cube_to_offset, hex_visible_false, hex_visible_true, ex_path_finding


class Exploring(Alone):
    def __init__(self, mob):
        Alone.__init__(self, mob)
        self.find = 0
        self.hexagon = False
        self.path = []
        self.step = get_ticks()

    def update(self, field):
        if not self.hexagon:
            self.hexagon = unexplored_finding(self.mob.coord, field, self.avoid)
        else:
            self.going(field)
        if self.hexagon:
            self.path = ex_path_finding(self.mob.coord, self.hexagon, field, self.avoid)
        return True

    def going(self, field):
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
        if self.hexagon:
            coord = hex_cube_to_offset(self.hexagon)
            if field.map[coord[0]][coord[1]][1].exploration:
                self.hexagon = False
            elif not self.path:
                self.hexagon = False
        return True
        #if get_ticks() - self.find >= self.mob.stats.find_time:
        #return 8


