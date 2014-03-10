from states.Alone import Alone


class Waiting(Alone):
    def __init__(self, mob):
        Alone.__init__(self, mob)
        self.hexagon = False
        self.quit = False

    def update(self, field):
        from pygame.constants import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONUP
        from pygame.event import poll, clear
        new_event = poll()
        if new_event.type == QUIT:
            self.quit = True
        elif new_event.type == KEYDOWN:
            if new_event.key == K_ESCAPE:
                from pygame.display import iconify
                iconify()
        elif new_event.type == MOUSEBUTTONUP:
            if new_event.button == 1:
                from Logic import pixel_to_hex, hex_cube_to_offset, hex_coord_available
                position = new_event.pos[0] + field.camera.border_pixel[0], new_event.pos[1] + field.camera.border_pixel[1]
                hexagon = pixel_to_hex(position, field.camera.size)
                coord = hex_cube_to_offset(hexagon)
                if hex_coord_available(hexagon, field) and field.map[coord[0]][coord[1]][1].exploration and \
                        field.map[coord[0]][coord[1]][1].passability:
                    self.hexagon = hexagon
        clear()
        return True

    def check(self, field):
        if self.hexagon:
            return 4
        return not self.quit
