from obj.Existence import Existence


class Cell(Existence):
    def __init__(self, coord):
        Existence.__init__(self, coord, False)

    @staticmethod
    def virtual_status_change():
        return True

    def virtual_image_name(self):
        return self.__class__.__name__ + '/' + self.__class__.__name__, 255