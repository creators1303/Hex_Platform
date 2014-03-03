from pygame.time import get_ticks
from Logic import path_finding, hex_cube_to_offset, neighbours_in_radius
from states.Attacking import Attacking
from states.Main import Main
from states.Merging import Merging


class Pursuit(Main):
    def __init__(self, mob, strike, field):
        Main.__init__(self, mob)
        self.strike = strike
        self.after = self.mob.stats.relationships[self.strike.__class__.__name__]
        self.step = get_ticks()

    def update(self, field, size):
        path = path_finding(self.mob.coord, self.strike.coord, field, self.mob.add_info)
        if not path:
            return 2
        if get_ticks() - self.step >= self.mob.stats.step_time:
            hexagon = path[0]
            coord = hex_cube_to_offset(hexagon)
            if not field.map[coord[0]][coord[1]][1].passability:
                field.map[coord[0]][coord[1]][1].virtual_status_change(0.5)
            else:
                self.mob.going(field, hexagon)
                self.step = get_ticks()
        return True

    def check(self, field):
        if not self.strike.alive:
            return 2
        nearest = neighbours_in_radius(self.mob.coord, 1, field)
        for each in nearest:
            if self.mob.stats.relationships[each.__class__.__name__] == "Attacking":
                self.mob.state = Attacking(self.mob, each)
                return True
            elif self.mob.stats.relationships[each.__class__.__name__] == "Merging":
                self.mob.state = Merging(self.mob, each)
                return True
        nearest = neighbours_in_radius(self.mob.coord, 3, field)
        for each in nearest:
            if not self.mob.relationships_check(each) and self.mob.stats.relationships[each.__class__.__name__] == "Attacking":
                self.mob.add_info.append(each)
        return True