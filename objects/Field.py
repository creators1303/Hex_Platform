from File import File
from Logic import __hex_offset_to_cube__, hex_to_pixel
from Graphic import Viewer
from objects.Cell import Cell
from objects.Door import Door
from objects.Mob import Mob
from objects.Player import Player
from objects.Wall import Wall
from objects.Supervisor import Supervisor


class Field():
    def __init__(self, screen):
        #TODO: странные циферки в конце файла
        #TODO: в файле не карта динамических объектов, а объекты по координатам
        #TODO: файл с параметрами генератора
        fields = File("FIELD.HMmap")
        self.rows, self.columns = list(map(int, fields.get_info(0)))
        size = list(map(int, File("GRAPHIC.HMinf").get_info(0)))
        self.screen = screen
        self.map = [[[[] for parameters in range(3)] for column in range(self.columns)] for row in range(self.rows)]
        self.objects = {}
        self.supervisors = []
        self.camera = None
        for row in range(1, self.rows + 1):
            static_cell = fields.get_info(row)
            dynamic_cell = fields.get_info(row + self.rows + 1)
            for column in range(self.columns):
                coord = __hex_offset_to_cube__(row - 1, column)
                self.map[row - 1][column][0] = coord
                self.map[row - 1][column][1] = static_objects(int(static_cell[column]), coord)
                self.map[row - 1][column][2] = hex_to_pixel(coord, size)
                self.dynamic_objects(int(dynamic_cell[column]), coord)

    def dynamic_objects(self, number, coord):
        if number == 1:
            thing = Player(coord)
            self.supervisors.append(Supervisor(thing))
            self.camera = Viewer(thing, self.screen)
            self.objects[coord] = thing
        elif number == 2:
            thing = Mob(coord)
            self.objects[coord] = thing
        else:
            #TODO: вставить исключение
            pass


def static_objects(number, coord):
    if number == 0:
        thing = Cell(coord)
    elif number == 1:
        thing = Wall(coord, False)
    elif number == 2:
        thing = Wall(coord, True)
    elif number == 3:
        thing = Door(coord)
    elif number == 4:
        thing = Wall(coord, False)
    else:
        #TODO: вставить исключение
        pass
    return thing

