from st.Alone import Alone


class Waiting(Alone):
    def __init__(self, mob):
        Alone.__init__(self, mob)
        self.hexagon = False
        self.quit = True

    def update(self, field):
        from pygame.constants import KEYDOWN, MOUSEBUTTONUP, K_EQUALS, K_MINUS, K_ESCAPE
        from pygame.event import poll, clear

        field.camera.set_lead(self.mob.leads[self.mob.current_lead])
        new_event = poll()
        if new_event.type == KEYDOWN:
            if new_event.key == K_EQUALS:
                self.mob.current_lead += 1
                self.mob.current_lead %= len(self.mob.leads)
            elif new_event.key == K_MINUS:
                self.mob.current_lead -= 1
                self.mob.current_lead %= len(self.mob.leads)
            elif new_event.key == K_ESCAPE:
                from bin.Interaction import pause_menu
                return pause_menu(field.screen, field)
        elif new_event.type == MOUSEBUTTONUP:
            if new_event.button == 1:
                from bin.Logic import pixel_to_hex, coord_get_offset, coord_available
                position = new_event.pos[0] + field.camera.border_pixel[0], new_event.pos[1] + field.camera.border_pixel[1]
                hexagon = pixel_to_hex(position, field.camera.size, field)
                coord = coord_get_offset(hexagon, field)
                if coord_available(hexagon, field) and field.map[coord[0]][coord[1]][1].exploration and \
                        field.map[coord[0]][coord[1]][1].passability:
                    self.hexagon = hexagon
        clear()
        return True
