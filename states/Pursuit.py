from states.Alone import Alone


class Pursuit(Alone):
    def __init__(self, mob):
        from pygame.time import get_ticks
        Alone.__init__(self, mob)
        self.find = 0
        self.strike = False
        self.path = []
        self.step = get_ticks()

    def update(self, field):
        if not self.strike:
            from Logic import neighbour_finding
            self.strike = neighbour_finding(self.mob.coord, field, self.avoid)
        else:
            #self.find = get_ticks()
            self.going(field)
        return True

    def going(self, field):
        from pygame.time import get_ticks
        from Logic import path_finding
        self.path = path_finding(self.mob.coord, self.strike.coord, field, self.avoid)
        if self.path and get_ticks() - self.step >= self.mob.stats.step_time:
            from Logic import coord_get_offset
            hexagon = self.path[0]
            coord = coord_get_offset(hexagon)
            if not field.map[coord[0]][coord[1]][1].passability:
                field.map[coord[0]][coord[1]][1].virtual_status_change(1)
            else:
                self.path = self.path[1:]
                self.mob.going(field, hexagon)
                self.step = get_ticks()
        return True

    def check(self, field):
        if self.strike:
            if self.strike.health <= 0 or self.strike in self.avoid:
                self.strike = False
        return True
        #if get_ticks() - self.find >= self.mob.stats.find_time:
        #return 8