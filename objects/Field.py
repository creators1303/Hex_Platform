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
        fields = File('FIELD.HMmap')
        size = fields.get_info(0)
        self.rows, self.columns = int(size[0]), int(size[1])
        size = File("GRAPHIC.HMinf")
        size = int(size.get_info(0)[0]), int(size.get_info(0)[1])
        self.screen = screen
        self.map = []
        self.objects = {}
        self.supervisors = []
        self.camera = None
        for ctrl_row in range(1, self.rows + 1):
            static_cell = fields.get_info(ctrl_row)
            dynamic_cell = fields.get_info(ctrl_row + self.rows + 1)
            temp_row = []
            for ctrl_column in range(self.columns):
                coord = __hex_offset_to_cube__((ctrl_row - 1, ctrl_column))
                temp_row.append([coord, static_objects(int(static_cell[ctrl_column]), coord), hex_to_pixel(coord, size)])
                if int(dynamic_cell[ctrl_column]):
                    self.objects[coord] = self.dynamic_objects(int(dynamic_cell[ctrl_column]), coord)
            self.map.append(temp_row)

    def dynamic_objects(self, number, coord):
        #TODO: РЕ разобраться с этим предупреждением
        if number == 1:
            thing = Player(coord)
            self.supervisors.append(Supervisor(thing))
            self.camera = Viewer(thing, self.screen)
        elif number == 2:
            thing = Mob(coord)
        return thing


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
    return thing

