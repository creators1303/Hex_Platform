from pygame.constants import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONUP
from pygame.display import iconify
from pygame.event import poll, clear
from Logic import pixel_to_hex, hex_cube_to_offset, hex_coord_available, neighbours_in_radius
from states.Attacking import Attacking
from states.Main import Main
from states.Walking import Walking


class Waiting(Main):
    def __init__(self, mob):
        Main.__init__(self, mob)

    def update(self, field, size):
        new_event = poll()
        if new_event.type == QUIT:
            return False
        elif new_event.type == KEYDOWN:
            if new_event.key == K_ESCAPE:
                iconify()
        elif new_event.type == MOUSEBUTTONUP:
            if new_event.button == 1:
                position = new_event.pos[0] + field.camera.border_pixel[0], new_event.pos[1] + field.camera.border_pixel[1]
                hexagon = pixel_to_hex(position, size)
                coord = hex_cube_to_offset(hexagon)
                if hex_coord_available(hexagon, field) and field.map[coord[0]][coord[1]][1].exploration and \
                        field.map[coord[0]][coord[1]][1].passability:
                    self.mob.state = Walking(self.mob, hexagon, field)
            if new_event.button == 3:
                position = new_event.pos[0] + field.camera.border_pixel[0], new_event.pos[1] + field.camera.border_pixel[1]
                hexagon = pixel_to_hex(position, size)
                coord = hex_cube_to_offset(hexagon)
                if hex_coord_available(hexagon, field) and field.map[coord[0]][coord[1]][1].exploration and \
                        field.map[coord[0]][coord[1]][1].passability_change:
                    self.mob.state = Walking(self.mob, hexagon, field)
        clear()
        return True

    def check(self, field):
        nearest = neighbours_in_radius(self.mob.coord, 1, field)
        for each in nearest:
            if self.mob.stats.relationships[each.__class__.__name__] == "Attacking":
                self.mob.state = Attacking(self.mob, each)
                break
        return True
