from objects.Existence import Existence


class Wall(Existence):
    def __init__(self, coord, destructible):
        Existence.__init__(self, coord)
        self.destructible = destructible

    @staticmethod
    def status_change():
        pass

    def virtual_image_name(self):
        if self.destructible:
            return self.__class__.__name__ + '/' + self.__class__.__name__, 255
        return self.__class__.__name__ + '/' + self.__class__.__name__ + '_indestructibility', 255
