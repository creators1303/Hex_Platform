from Logic import hex_cube_to_offset
from File import File


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

    def image_status(self):
        if not self.exploration:
            return False, False, False, 'fog/' + 'fog_incognito', 255
        if not self.visibility:
            return True, False, False, 'fog/' + 'fog_war', 150
        if self.visibility == 1:
            return True, True, False, 'fog/' + 'fog', 50
        return True, True, True, False

    def virtual_image_name(self):
        return 'error'
        #TODO: заменить на исключение
