from Logic import hex_cube_to_offset
from File import File
from states.Exploring import Exploring
from states.Waiting import Waiting
from states.Despawning import Despawning
from states.Attacking import Attacking
from states.Merging import Merging
from states.Pursuit import Pursuit


class Existence():
    def __init__(self, coord, state):
        parameters = File(self.__class__.__name__ + '/' + "PARAMETERS.HMinf")
        info = {}
        for each in parameters.info:
            each = each.split(" ")
            info[each[0]] = int(each[1])
        self.alone_state = state
        self.communication_state = False
        self.current_state = self.alone_state
        self.coord = coord
        self.offset_coord = hex_cube_to_offset(coord)
        self.passability = info["passability"]
        self.transparency = info["transparency"]
        self.passability_change = info["passability_change"]
        self.level = info["level"]
        self.health = info["health"]
        self.exploration = False
        self.visibility = False

    def going(self, field, hexagon):
        if not hexagon in field.objects:
            field.objects[hexagon] = self
            del (field.objects[self.coord])
            self.coord = hexagon
            self.offset_coord = hex_cube_to_offset(hexagon)

    def relationships_check(self, mob):
        if mob.health > self.health:
            return False
        return True

    def visible_change(self, status):
        self.visibility = status
        if status:
            self.exploration = True

    def update(self, field):
        self.current_state.global_update(field)

    def state_check(self, field):
        status = self.current_state.global_check(field)
        if status == 2:
            strike = self.current_state.communication
            self.communication_state = Attacking(self, strike)
            self.current_state = self.communication_state
        elif status == 3:
            strike = self.current_state.communication
            self.communication_state = Merging(self, strike)
            self.current_state = self.communication_state
        else:
            if status == 5:
                self.alone_state = Waiting(self)
            elif status == 6:
                self.alone_state = Exploring(self)
            elif status == 7:
                self.alone_state = Pursuit(self)
            elif status == 8:
                self.alone_state = Despawning(self)
            elif status == 9:
                self.current_state = self.alone_state
            self.current_state = self.alone_state

    def alive_check(self, field):
        if self.health <= 0:
            del (field.objects[self.coord])

    def image_status(self):
        if not self.exploration:
            return False, False, False, 'fog/' + 'fog_incognito', 255
        if not self.visibility:
            return True, False, False, 'fog/' + 'fog_war', 150
        if self.visibility == 1:
            return True, True, False, 'fog/' + 'fog', 50
        return True, True, True, False
