from pygame.constants import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONUP
from pygame.display import iconify
from pygame.event import poll, clear
from Logic import pixel_to_hex, hex_cube_to_offset, hex_coord_available, neighbours_in_radius
from states.Alone import Alone


class Waiting(Alone):
    def __init__(self, mob):
        Alone.__init__(self, mob)
        self.hexagon = False
        self.quit = False

    def update(self, field):
        new_event = poll()
        if new_event.type == QUIT:
            self.quit = True
        elif new_event.type == KEYDOWN:
            if new_event.key == K_ESCAPE:
                iconify()
        elif new_event.type == MOUSEBUTTONUP:
            if new_event.button == 1:
                position = new_event.pos[0] + field.camera.border_pixel[0], new_event.pos[1] + field.camera.border_pixel[1]
                hexagon = pixel_to_hex(position, field.camera.size)
                coord = hex_cube_to_offset(hexagon)
                if hex_coord_available(hexagon, field) and field.map[coord[0]][coord[1]][1].exploration and \
                        field.map[coord[0]][coord[1]][1].passability:
                    self.hexagon = hexagon
            '''if new_event.button == 3:
                position = new_event.pos[0] + field.camera.border_pixel[0], new_event.pos[1] + field.camera.border_pixel[1]
                hexagon = pixel_to_hex(position, field.camera.size)
                coord = hex_cube_to_offset(hexagon)
                if hex_coord_available(hexagon, field) and field.map[coord[0]][coord[1]][1].exploration and \
                        field.map[coord[0]][coord[1]][1].passability_change:
                    self.hexagon = hexagon'''
        clear()
        return True

    def check(self, field):
        if self.hexagon:
            return 4
        return not self.quit
