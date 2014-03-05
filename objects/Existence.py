from Logic import hex_cube_to_offset
from File import File
from states.Walking import Walking
from states.Exploring import Exploring
from states.Waiting import Waiting
from states.Despawning import Despawning
from states.Attacking import Attacking
from states.Merging import Merging


class Existence():
    def __init__(self, coord):
        parameters = File(self.__class__.__name__ + '/' + "PARAMETERS.HMinf")
        info = {}
        for each in parameters.info:
            each = each.split(" ")
            info[each[0]] = int(each[1])
        self.coord = coord
        self.offset_coord = hex_cube_to_offset(coord)
        self.passability = info["passability"]
        self.transparency = info["transparency"]
        self.passability_change = info["passability_change"]
        self.level = info["level"]
        self.health = info["health"]
        self.exploration = False
        self.visibility = False
        self.alive = True

    def going(self, field, hexagon):
        if not hexagon in field.objects:
            field.objects[hexagon] = self
            del(field.objects[self.coord])
            self.coord = hexagon
            self.offset_coord = hex_cube_to_offset(hexagon)

    @staticmethod
    def relationships_check(mob):
        return True

    def visible_change(self, status):
        self.visibility = status
        if status:
            self.exploration = True

    def image_name(self):
        #TODO: попробовать убрать эту функцию, вызывать сразу виртуальную
        return self.virtual_image_name()

    def update(self, field):
        status = self.state.global_update(field)
        return status

    def state_check(self, field):
        if not self.alive:
            del field.objects[self.coord]
        else:
            status = self.state.global_check(field)
            if status == 2:
                strike = self.state.communication
                self.state = Attacking(self, strike)
            if status == 3:
                strike = self.state.communication
                self.state = Merging(self, strike)
            if status == 4:
                hexagon = self.state.hexagon
                self.state = Walking(self, hexagon, field)
            if status == 5:
                self.state = Waiting(self)
            if status == 6:
                self.state = Exploring(self, [])
            if status == 8:
                self.state = Despawning(self)
            return status

    def alive_check(self, field):
        if not self.alive:
            del(field.objects[self.coord])

    def image_status(self):
        if not self.exploration:
            return False, False, False, 'fog/' + 'fog_incognito', 255
        if not self.visibility:
            return True, False, False, 'fog/' + 'fog_war', 150
        if self.visibility == 1:
            return True, True, False, 'fog/' + 'fog', 50
        return True, True, True, False
