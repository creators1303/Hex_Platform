from File import File
from objects.Existence import Existence
from objects.Stats import Stats
from states.PrimaryPlayer import PrimaryPlayer
from states.Waiting import Waiting


class Player(Existence):
    def __init__(self, coord):
        #TODO: заменить СТАТУС на набор параметров
        self.id = True
        Existence.__init__(self, coord, False, False, 5)
        #TODO: заменить на имя класса
        self.stats = Stats(File("Player/" + "SKILLS.HMinf"), File("Player/" + "RELATIONSHIPS.HMinf"))
        self.state = PrimaryPlayer(self)

    def update(self, field, size):
        status = self.state.update(field, size)
        if status == 2:
            self.state = Waiting(self)
        if status == 3:
            return False
        return status

    def check(self, field):
        if not self.alive:
            del field.objects[self.coord]
        else:
            status = self.state.check(field)
            return status

    @staticmethod
    def status_change():
        pass

    def virtual_image_name(self):
        return self.__class__.__name__ + '/' + self.__class__.__name__, 255  # , str(self.level)
