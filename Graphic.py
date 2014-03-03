from pygame.display import flip
from pygame.font import Font
from Worker import object_image_load
from File import File


class ImageStorage():

    def __init__(self):
        self.storage = {}

    def get_image(self, parameters):
        if not parameters[0] + '.HMtex' in self.storage.keys():
            self.load_image(parameters)
        return self.storage[parameters[0] + '.HMtex']

    def load_image(self, parameters):
        self.storage[parameters[0] + '.HMtex'] = object_image_load(parameters)


class Viewer():
    def __init__(self, player, screen):

        graphics = File("GRAPHIC.HMinf")
        self.size = int(graphics.get_info(0)[0]), int(graphics.get_info(0)[1])

        self.cols = screen.get_width() - self.size[0] * 0.25
        self.border_width = int((self.cols % (self.size[0] * 0.75)) / 2)
        self.cols = int((self.cols - self.border_width * 2) / (self.size[0] * 0.75))

        self.rows = screen.get_height() - self.size[1] / 2
        self.border_height = int((self.rows % self.size[1]) / 2)
        self.rows = int((self.rows - self.border_height * 2) / self.size[1])

        self.zone_rows = int(self.rows / 2) + (int(self.rows / 2) + 1) % 2
        self.zone_cols = int(self.cols / 2) + (int(self.cols / 2) + 1) % 2

        self.point = [int(player.offset_coord[0] - (self.zone_rows - 1) / 2), int(player.offset_coord[1] - (self.zone_cols - 1) / 2)]

        self.lead = player

        self.border_from = False
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
        self.border_from = [self.point[0] - int((self.rows - self.zone_rows) / 2), self.point[1] - int((self.cols - self.zone_cols) / 2)]
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
        screen.fill((0, 0, 150))
        font = Font(None, 20)
        self.movement_check(field)
        for ctrl_row in range(self.border_from[0], self.border_to[0] + 1):
            for ctrl_column in range(self.border_from[1], self.border_to[1] + 1):
                parameters = field.map[ctrl_row][ctrl_column][1].image_status()
                pixel = field.map[ctrl_row][ctrl_column][2][0] - self.border_pixel[0] + self.border_width, \
                        field.map[ctrl_row][ctrl_column][2][1] - self.border_pixel[1] + self.border_height
                if parameters[0]:
                    picture = list(field.map[ctrl_row][ctrl_column][1].image_name())
                    picture.append(self.size)
                    screen.blit(animation.get_image(picture), pixel)
                if parameters[3]:
                    parameters = list(parameters[3:])
                    parameters.append(self.size)
                    screen.blit(animation.get_image(parameters), pixel)
        for dynamic_object in field.objects.values():
            parameters = field.map[dynamic_object.offset_coord[0]][dynamic_object.offset_coord[1]][1].image_status()
            if self.border_from[0] <= dynamic_object.offset_coord[0] <= self.border_to[0] and self.border_from[1] <= \
                    dynamic_object.offset_coord[1] <= self.border_to[1]:
                pixel = field.map[dynamic_object.offset_coord[0]][dynamic_object.offset_coord[1]][2][0] - self.border_pixel[0] + self.border_width, \
                        field.map[dynamic_object.offset_coord[0]][dynamic_object.offset_coord[1]][2][1] - self.border_pixel[1] + self.border_height
                if parameters[1]:
                    picture = list(dynamic_object.image_name())
                    picture.append(self.size)
                    screen.blit(animation.get_image(picture), pixel)
                    if parameters[2]:
                        text = font.render(str(dynamic_object.level), 1, (255, 255, 0))
                        screen.blit(text, pixel)
                        text = font.render(str(dynamic_object.health), 1, (255, 0, 0))
                        screen.blit(text, (pixel[0] + self.size[0] * 0.75, pixel[1]))
        flip()
