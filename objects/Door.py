from pygame.time import get_ticks
from objects.Existence import Existence


class Door(Existence):
    def __init__(self, coord, status):
        #TODO: заменить СТАТУС на набор параметров
        Existence.__init__(self, coord, status, True, 0)
        self.opening = 0
        self.opening_time = False
        self.hard = 500

    def virtual_status_change(self, power):
        if not self.opening_time:
            self.opening_time = get_ticks()
        self.opening = (get_ticks() - self.opening_time) * power
        if self.opening > self.hard:
            self.opening = 0
            self.opening_time = False
            self.passability = (self.passability + 1) % 2
            self.transparency = self.passability

    def virtual_image_name(self):
        #TODO: заменить на имя класса
        if self.passability:
            return 'Door/' + 'door_open', 255  # , ''
        return 'Door/' + 'door_close', 255  # , ''
