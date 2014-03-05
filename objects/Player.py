from objects.Existence import Existence
from objects.Stats import Stats
from states.PrimaryPlayer import PrimaryPlayer



class Player(Existence):
    def __init__(self, coord):
        Existence.__init__(self, coord)
        self.stats = Stats(self)
        self.state = PrimaryPlayer(self)

    @staticmethod
    def status_change():
        pass

    def virtual_image_name(self):
        return self.__class__.__name__ + '/' + self.__class__.__name__, 255
