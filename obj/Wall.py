from obj.Existence import Existence


class Wall(Existence):
    def __init__(self, coord, destructible, field):
        Existence.__init__(self, coord, False, field)
        self.destructible = destructible

    def virtual_status_change(self, power):
        pass

    def virtual_image_name(self):
        if self.destructible:
            return self.__class__.__name__ + '/' + self.__class__.__name__, 255
        return self.__class__.__name__ + '/' + self.__class__.__name__ + '_indestructible', 255
