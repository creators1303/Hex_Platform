from pygame.time import get_ticks
from states.Alone import Alone
from Logic import unexplored_finding, hex_cube_to_offset, hex_visible_false, hex_visible_true, ex_path_finding

#TODO: время: поиска пути(если не нашел, то новый гекс) и гекса(если не нашел, то умер)


class Exploring(Alone):
    def __init__(self, mob):
        Alone.__init__(self, mob)
        self.hexagon = False
        self.step_time = None
        self.find_time = get_ticks()
        self.path_time = get_ticks()

    def update(self, field):
        if not self.hexagon:
            self.hexagon = unexplored_finding(self.mob.coord, field, self.avoid)
            self.step_time = get_ticks()
            #print("Finding", self.hexagon)
        else:
            #print("Found", self.hexagon)
            self.find_time = get_ticks()
            path = ex_path_finding(self.mob.coord, self.hexagon, field, self.avoid)
            if path:
                #print("Going", path)
                self.path_time = get_ticks()
                self.going(field, path)
            else:
                self.step_time = get_ticks()
        return True

    def going(self, field, path):
        if get_ticks() - self.step_time >= self.mob.stats.step_time:
            coord = hex_cube_to_offset(path)
            if not field.map[coord[0]][coord[1]][1].passability:
                field.map[coord[0]][coord[1]][1].virtual_status_change(1)
            else:
                hex_visible_false(field, self.mob.coord, self.mob.stats.view_radius)
                self.mob.going(field, path)
                hex_visible_true(field, self.mob.coord, self.mob.stats.view_radius)
                self.step_time = get_ticks()
        return True

    def check(self, field):
        if self.hexagon:
            coord = hex_cube_to_offset(self.hexagon)
            if field.map[coord[0]][coord[1]][1].exploration:
                #print("Explored")
                self.hexagon = False
        if get_ticks() - self.find_time >= self.mob.stats.find_time:
            return 8
        if get_ticks() - self.path_time >= self.mob.stats.path_time:
            self.path_time = get_ticks()
            self.hexagon = False
        return True


