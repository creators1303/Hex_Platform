from objects.Existence import Existence
from objects.Stats import Stats
from states.PrimaryAntagonist import PrimaryAntagonist


class Antagonist(Existence):

    def __init__(self, coord):
        Existence.__init__(self, coord, PrimaryAntagonist(self))
        self.stats = Stats(self)

    @staticmethod
    def status_change():
        pass

    def virtual_image_name(self):
        return self.__class__.__name__ + '/' + 'self', 255
