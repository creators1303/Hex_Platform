from bin.File import File


class Menu:
    def __init__(self, buttons, screen, text_color, selection_color, surface, font_size=120):
        from pygame.font import Font

        self.buttons = buttons
        self.number_buttons = len(self.buttons)
        self.info_list = [self.Text() for parameters in range(self.number_buttons)]
        self.font_size = font_size
        self.text_color = text_color
        self.selection_color = selection_color
        self.surface_color = surface
        self.current_position = 0
        self.shift = (200, 0)
        self.menu_width = 0
        self.menu_height = 0
        self.surface = screen
        self.font = Font(None, self.font_size)

        for i in range(self.number_buttons):
            self.info_list[i].text = self.buttons[i]
            self.info_list[i].text_surface = self.font.render(self.info_list[i].text, 1, self.text_color)

            self.info_list[i].text_rect = self.info_list[i].text_surface.get_rect()
            shift = int(self.font_size * 0.3)

            height = self.info_list[i].text_rect.height
            self.info_list[i].text_rect.left = shift
            self.info_list[i].text_rect.top = shift + (shift * 2 + height) * i

            width = self.info_list[i].text_rect.width + shift * 2
            height = self.info_list[i].text_rect.height + shift * 2

            left = self.info_list[i].text_rect.left - shift
            top = self.info_list[i].text_rect.top - shift

            self.info_list[i].point_rect = (left, top, width, height)
            if width > self.menu_width:
                self.menu_width = width
            self.menu_height += height
        x = self.surface.get_rect().centerx - self.menu_width / 2
        y = self.surface.get_rect().centery - self.menu_height / 2
        self.shift = (x + self.shift[0], y + self.shift[1])

    class Text:
        text = ""
        text_surface = None
        text_rect = None
        point_rect = None

    def get_position(self):
        return self.current_position

    def draw(self, pressed):
        from pygame.surface import Surface
        from pygame.draw import rect
        from pygame.display import flip

        self.surface.fill(self.surface_color)
        if pressed:
            self.current_position += pressed
            self.current_position %= self.number_buttons
        menu_surface = Surface((self.menu_width, self.menu_height))
        menu_surface.fill(self.surface_color)
        rect(menu_surface, self.selection_color, self.info_list[self.current_position].point_rect)
        for i in range(self.number_buttons):
            menu_surface.blit(self.info_list[i].text_surface, self.info_list[i].text_rect)
        self.surface.blit(menu_surface, self.shift)
        flip()

    def update(self):
        from pygame.constants import KEYDOWN, K_UP, K_DOWN, K_RETURN
        from pygame.event import poll

        self.draw(0)
        while True:
            event = poll()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    self.draw(-1)
                if event.key == K_DOWN:
                    self.draw(1)
                if event.key == K_RETURN:
                    return self.get_position()
        return -1


class ColorStorage():
    def __init__(self):
        from json import load
        file = open("res/colors.json", "r")
        self.palette = load(file)

    def get_color(self, name):
        return self.palette[name]


class ImageStorage():
    def __init__(self):
        self.storage = {}

    def get_image(self, parameters):
        if not parameters[0] + '.bmp' in self.storage.keys():
            self.load_image(parameters)
        return self.storage[parameters[0] + '.bmp']

    def load_image(self, parameters):
        from bin.Worker import object_image_load

        self.storage[parameters[0] + '.bmp'] = object_image_load(parameters)


class Viewer():
    def __init__(self, screen):

        self.size = list(map(int, File("GRAPHIC.HMinf").get_info(0)))

        self.cols = screen.get_width() - self.size[0] // 4
        self.border_width = self.cols % int(self.size[0] * 0.75) // 2
        self.cols = (self.cols - self.border_width * 2) // int(self.size[0] * 0.75)

        self.rows = screen.get_height() - self.size[1] // 2
        self.border_height = self.rows % self.size[1] // 2
        self.rows = (self.rows - self.border_height * 2) // self.size[1]

        self.zone_rows = self.rows // 2 + (self.rows // 2 + 1) % 2
        self.zone_cols = self.cols // 2 + (self.cols // 2 + 1) % 2
        self.point = None
        self.lead = None
        self.border_from = [None, None]
        self.border_to = None
        self.border_pixel = None

    def set_lead(self, lead):
        if self.lead != lead:
            self.point = [lead.offset_coord[0] - (self.zone_rows - 1) // 2,
                          lead.offset_coord[1] - (self.zone_cols - 1) // 2]
            self.lead = lead
            self.border_from = [False, False]
            self.border_to = False
            self.border_pixel = False

    def movement_check(self, field):
        if self.lead.offset_coord[0] < self.point[0]:
            self.point[0] -= 1
        elif self.lead.offset_coord[0] >= self.point[0] + self.zone_rows:
            self.point[0] += 1
        if self.lead.offset_coord[1] < self.point[1]:
            self.point[1] -= 1
        elif self.lead.offset_coord[1] >= self.point[1] + self.zone_cols:
            self.point[1] += 1
        self.border_from = [self.point[0] - (self.rows - self.zone_rows) // 2,
                            self.point[1] - (self.cols - self.zone_cols) // 2]
        if self.border_from[0] < 0:
            self.border_from[0] = 0
        if self.border_from[1] < 0:
            self.border_from[1] = 0
        self.border_to = [self.border_from[0] + self.rows - 1, self.border_from[1] + self.cols - 1]
        if self.border_to[0] >= field.rows:
            self.border_to[0] = field.rows - 1
            self.border_from[0] = self.border_to[0] - self.rows + 1
        if self.border_to[1] >= field.columns:
            self.border_to[1] = field.columns - 1
            self.border_from[1] = self.border_to[1] - self.cols + 1

        self.border_pixel = field.map[self.border_from[0]][self.border_from[1]][2]
        if not self.border_from[1] % 2:
            self.border_pixel = (self.border_pixel[0], self.border_pixel[1] - self.size[1] / 2)

    def draw_field(self, screen, field, animation):
        from pygame.display import flip
        from pygame.font import Font

        screen.fill((50, 50, 30))
        font = Font(None, 20)
        self.movement_check(field)
        for ctrl_row in range(self.border_from[0], min(self.border_to[0] + 1, field.rows)):
            for ctrl_column in range(self.border_from[1], min(self.border_to[1] + 1, field.columns)):
                parameters = field.map[ctrl_row][ctrl_column][1].image_status()
                pixel = field.map[ctrl_row][ctrl_column][2][0] - self.border_pixel[0] + self.border_width, \
                        field.map[ctrl_row][ctrl_column][2][1] - self.border_pixel[1] + self.border_height
                if parameters[0]:
                    picture = list(field.map[ctrl_row][ctrl_column][1].virtual_image_name())
                    picture.append(self.size)
                    screen.blit(animation.get_image(picture), pixel)
                if parameters[3]:
                    parameters = list(parameters[3:])
                    parameters.append(self.size)
                    screen.blit(animation.get_image(parameters), pixel)
        for dynamic_object in field.objects.values():
            coord = dynamic_object.offset_coord
            if self.border_from[0] <= coord[0] <= self.border_to[0] and self.border_from[1] <= coord[1] <= \
                    self.border_to[1]:
                parameters = field.map[dynamic_object.offset_coord[0]][dynamic_object.offset_coord[1]][1].image_status()
                pixel = field.map[coord[0]][coord[1]][2][0] - self.border_pixel[0] + self.border_width, \
                        field.map[coord[0]][coord[1]][2][1] - self.border_pixel[1] + self.border_height
                if parameters[1]:
                    picture = list(dynamic_object.virtual_image_name())
                    picture.append(self.size)
                    screen.blit(animation.get_image(picture), pixel)
                    if parameters[2]:
                        text = font.render(str(dynamic_object.level), 1, (255, 255, 0))
                        screen.blit(text, pixel)
                        text = font.render(str(dynamic_object.health), 1, (255, 0, 0))
                        screen.blit(text, (pixel[0] + self.size[0] * 0.75, pixel[1]))
        flip()
