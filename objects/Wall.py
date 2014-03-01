from objects.Existence import Existence


class Wall(Existence):
    def __init__(self, coord, status, destructible):
        #TODO: заменить СТАТУС на набор параметров
        Existence.__init__(self, coord, status, False, 0)
        self.destructible = destructible
        #TODO: перенести этот параметр в Existence

    @staticmethod
    def status_change():
        pass

    def virtual_image_name(self):
        #TODO: заменить на имя класса
        if self.destructible:
            return 'Wall/' + 'Wall', 255  # , ''
        return 'Wall/' + 'wall_indestructibility', 255,  # ''
