from obj.Existence import Existence


class Cell(Existence):
    def __init__(self, coord, field):
        Existence.__init__(self, coord, False, field)

    def virtual_status_change(self, power):
        return True

    def virtual_image_name(self):
        return self.__class__.__name__ + '/' + self.__class__.__name__, 255