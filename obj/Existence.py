from st.Attacking import Attacking
from st.Despawning import Despawning
from st.Exploring import Exploring
from st.Merging import Merging
from st.Pursuit import Pursuit


class Existence():
    def __init__(self, coord, state, field):
        from bin.Logic import coord_get_offset
        from json import load
        self.alone_state = state
        self.communication_state = False
        self.current_state = self.alone_state
        self.coord = coord
        self.offset_coord = coord_get_offset(coord, field)
        file = open("res/" + self.__class__.__name__ + "/" + "PARAMETERS.json")
        parameters = load(file)
        file.close()
        self.passability = parameters["passability"]
        self.transparency = parameters["transparency"]
        self.passability_change = parameters["passability_change"]
        self.level = parameters["level"]
        self.health = parameters["health"]
        self.exploration = False
        self.visibility = False

    def going(self, field, hexagon):
        if not hexagon in field.objects:
            from bin.Logic import coord_get_offset
            field.objects[hexagon] = self
            del (field.objects[self.coord])
            self.coord = hexagon
            self.offset_coord = coord_get_offset(hexagon, field)
        else:
            print('BUG HERE')

    def relationships_check(self, mob):
        if mob.health >= self.health:
            return False
        return True

    def visible_change(self, status):
        self.visibility = status
        if status:
            self.exploration = True

    def state_update(self, field):
        self.current_state.global_update(field)

    def state_check(self, field):
        status = self.current_state.global_check(field)
        if status == 1:
            return
        if status == 2:
            strike = self.current_state.communication
            self.communication_state = Attacking(self, strike)
            self.current_state = self.communication_state
        elif status == 3:
            strike = self.current_state.communication
            self.communication_state = Merging(self, strike)
            self.current_state = self.communication_state
        else:
            if status == 6:
                self.alone_state = Exploring(self)
            elif status == 7:
                self.alone_state = Pursuit(self)
            elif status == 8:
                self.alone_state = Despawning(self)
            self.current_state = self.alone_state

    def alive_check(self, field):
        if self.health <= 0:
            from bin.Logic import hex_visible_false
            hex_visible_false(field, self.coord, self.stats.view_radius)
            del field.objects[self.coord]

    def image_status(self):
        if not self.exploration:
            return False, False, False, 'Fog/' + 'Fog_incognito', 255
        if not self.visibility:
            return True, False, False, 'Fog/' + 'Fog_war', 150
        if self.visibility == 1:
            return True, True, False, 'Fog/' + 'Fog', 50
        return True, True, True, False
