from objects.Existence import Existence
from objects.Stats import Stats
from states.PrimaryMob import PrimaryMob
from states.Finding import Finding


class Mob(Existence):

    def __init__(self, coord):
        Existence.__init__(self, coord)
        self.state = PrimaryMob(self)
        self.stats = Stats(self)
        self.add_info = []

    def update(self, field):
        status = self.state.update(field)
        if status == 2:
            self.state = Finding(self, self.add_info)
        return status

    def check(self, field):
        if not self.alive:
            del field.objects[self.coord]
        else:
            status = self.state.check(field)
            if status == 2:
                self.state = Finding(self, self.add_info)

    @staticmethod
    def status_change():
        pass

    def virtual_image_name(self):
        return self.__class__.__name__ + '/' + self.__class__.__name__, 255
