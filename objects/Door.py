from pygame.time import get_ticks
from objects.Existence import Existence


class Door(Existence):
    def __init__(self, coord):
        Existence.__init__(self, coord, False)
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
        if self.passability:
            return self.__class__.__name__ + '/' + self.__class__.__name__ + '_open', 255
        return self.__class__.__name__ + '/' + self.__class__.__name__ + '_close', 255
