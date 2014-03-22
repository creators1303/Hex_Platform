from bin.Logic import coord_get_cube, hex_to_pixel
from bin.Graphic import Viewer
from bin.File import File
from obj.Antagonist import Antagonist
from obj.Protagonist import Protagonist
from obj.Cell import Cell
from obj.Wall import Wall
from obj.Door import Door
from obj.Supervisor import Supervisor



class Field():
    def __init__(self, screen):
        #TODO: в файле не карта динамических объектов, а объекты по координатам
        fields = File("FIELD.HMmap")
        self.rows, self.columns = list(map(int, fields.get_info(0)))
        size = list(map(int, File("GRAPHIC.HMinf").get_info(0)))
        self.screen = screen
        self.map = [[[[] for parameters in range(3)] for column in range(self.columns)] for row in range(self.rows)]
        self.objects = {}
        self.supervisors = [Supervisor()]
        self.camera = Viewer(screen)
        self.coord_dict = {}
        for row in range(1, self.rows + 1):
            static_cell = fields.get_info(row)
            dynamic_cell = fields.get_info(row + self.rows + 1)
            for column in range(self.columns):
                coord = coord_get_cube(row - 1, column)
                self.coord_dict[coord] = (row - 1, column)
                self.map[row - 1][column][0] = coord
                self.map[row - 1][column][1] = self.static_objects(int(static_cell[column]), coord)
                self.map[row - 1][column][2] = hex_to_pixel(coord, size, self)
                self.dynamic_objects(int(dynamic_cell[column]), coord)

    def dynamic_objects(self, number, coord):
        if number == 1:
            thing = Protagonist(coord, self)
            self.objects[coord] = thing
            self.supervisors[0].add_lead(thing)
        elif number == 2:
            thing = Antagonist(coord, self)
            self.objects[coord] = thing
        else:
            #TODO: вставить исключение
            pass

    def static_objects(self, number, coord):
        if number == 0:
            thing = Cell(coord, self)
        elif number == 1:
            thing = Wall(coord, False, self)
        elif number == 2:
            thing = Wall(coord, True, self)
        elif number == 3:
            thing = Door(coord, self)
        elif number == 4:
            thing = Wall(coord, False, self)
        else:
            #TODO: вставить исключение
            pass
        return thing

