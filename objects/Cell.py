from objects.Existence import Existence


class Cell(Existence):
    def __init__(self, coord, status):
        #TODO: заменить СТАТУС на набор параметров
        Existence.__init__(self, coord, status, True, 0)

    @staticmethod
    def virtual_status_change():
        return True

    def virtual_image_name(self):
        #TODO: заменить на имя класса
        return 'Cell/' + 'Cell', 255  # , ''
