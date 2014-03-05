from pygame.time import get_ticks
from Logic import path_finding, hex_cube_to_offset, neighbour_finding
from states.Alone import Alone


class Pursuit(Alone):
    def __init__(self, mob, avoid):
        Alone.__init__(self, mob)
        self.strike = False
        self.step = get_ticks()
        self.avoid = avoid

    def update(self, field):
        if not self.strike:
            self.strike = neighbour_finding(self.mob.coord, field, self.avoid)
        else:
            self.going(field)
        return True

    def going(self, field):
        path = path_finding(self.mob.coord, self.strike.coord, field, self.mob.add_info)
        if path and get_ticks() - self.step >= self.mob.stats.step_time:
            hexagon = path[0]
            coord = hex_cube_to_offset(hexagon)
            if not field.map[coord[0]][coord[1]][1].passability:
                field.map[coord[0]][coord[1]][1].virtual_status_change(0.5)
            else:
                self.mob.going(field, hexagon)
                self.step = get_ticks()

    def check(self, field):
        if self.strike:
            if not self.strike.alive:
                self.strike = False
        return True