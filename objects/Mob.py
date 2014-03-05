from objects.Existence import Existence
from objects.Stats import Stats
from states.PrimaryMob import PrimaryMob


class Mob(Existence):

    def __init__(self, coord):
        Existence.__init__(self, coord)
        self.state = PrimaryMob(self)
        self.stats = Stats(self)
        self.add_info = []

    @staticmethod
    def status_change():
        pass

    def virtual_image_name(self):
        return self.__class__.__name__ + '/' + self.__class__.__name__, 255
