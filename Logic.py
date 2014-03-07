from math import sqrt, degrees, atan
from operator import itemgetter


def __line_length__(coord1, coord2):
    """
    @param coord1: cube coord of first hex
    @param coord2: cube coord of second hex
    @return: logic line length of line between first and second hexes
    """
    logic_coord1 = __hex_to_coord__(coord1, (0, 0))
    logic_coord2 = __hex_to_coord__(coord2, (0, 0))
    return sqrt(pow(logic_coord1[0] - logic_coord2[0], 2) + pow(logic_coord1[1] - logic_coord2[1], 2))


def hex_to_pixel(coord, size):
    """
    @param coord: cube coord of hex
    @param size: size of the image of hex
    @return: XY coord of the start drawing point
    """
    coord = hex_cube_to_offset(coord)
    return int(coord[1] * size[0] * 0.75), int(size[1] * coord[0] + size[1] * 0.5 * ((coord[1] + 1) % 2))


def hex_distance(coord1, coord2):
    """
    @param coord1: cube coord of start hex
    @param coord2: cube coord of goal hex
    @return: distance in steps between two hexes
    """
    return max(abs(coord1[0] - coord2[0]), abs(coord1[1] - coord2[1]), abs(coord1[2] - coord2[2]))


def __hex_to_coord__(coord, shift):
    """
    @param coord: cube coord of hex
    @param shift: XY coord of shift (to angle or to center)
    @return: XY coord of the logic up-left angle of surface + shift
    """
    return coord[0] * 0.75 + shift[0], \
           (0.5 * ((coord[0] + 1) % 2) + int((coord[0] + 1) / 2) + coord[1]) * sqrt(3) / 2 + shift[1]


def __hex_offset_to_cube__(coord):
    """
    @param coord: offset coord of hex
    @return: cube coord of hex
    """
    x = int(coord[1])
    y = int(coord[0] - (coord[1] + (coord[1] & 1)) / 2)
    return x, y, (x + y) * -1


def hex_cube_to_offset(coord):
    """
    @param coord: cube coord of hex
    @return: offset coord of hex
    """
    return int((coord[0] + 1) / 2) + coord[1], coord[0]


def __hex_neighbours__(coord):
    """
    @param coord: cube coord of hex
    @return: cube coord of neighbours
    """
    #TODO: может лучше брать из файла один раз?
    neighbours_coord = [(0, -1, 1), (1, -1, 0), (1, 0, -1), (0, 1, -1), (-1, 1, 0), (-1, 0, 1)]
    neighbours = []
    for neighbour in neighbours_coord:
        neighbours.append((coord[0] + neighbour[0], coord[1] + neighbour[1], coord[2] + neighbour[2]))
    return neighbours


def pixel_to_hex(coord, size):
    """
    @param coord: XY coord of point
    @return: cube coord of hex
    """
    x_coord = coord[0] / size[0]
    y_coord = coord[1] / size[1]
    coord = (x_coord, y_coord)
    x = int(x_coord / 0.75)
    y = int(y_coord - ((x + 1) % 2) * 0.45)
    hexagon = __hex_offset_to_cube__((y, x))
    logic_coord1 = __hex_to_coord__(hexagon, (0.5, 0.45))
    logic_coord2 = __hex_to_coord__((hexagon[0] - 1, hexagon[1], hexagon[2] + 1), (0.5, 0.45))
    logic_coord3 = __hex_to_coord__((hexagon[0] - 1, hexagon[1] + 1, hexagon[2]), (0.5, 0.45))
    line1 = __line_length__(coord, logic_coord1)
    line2 = __line_length__(coord, logic_coord2)
    line3 = __line_length__(coord, logic_coord3)
    if line1 < line2 and line1 < line3:
        return hexagon
    if line2 < line1 and line2 < line3:
        return hexagon[0] - 1, hexagon[1], hexagon[2] + 1
    return hexagon[0] - 1, hexagon[1] + 1, hexagon[2]


def hex_coord_available(coord, field):
    """
    @param coord: cube coord of hex
    @param field: field object to find map size
    @return: (True) if there exists hex with this coord, else (False)
    """
    coord = hex_cube_to_offset(coord)
    if 0 <= coord[0] < field.rows and 0 <= coord[1] < field.columns:
        return True
    return False


def __hex_radius__(coord, radius, field):
    """
    @param coord: cube coord of hex
    @param radius: radius in hexes
    @param field: field object
    @return: all hexes in radius
    """
    coord_list = []
    for x in range(coord[0] - radius, coord[0] + radius + 1):
        for y in range(coord[1] - radius, coord[1] + radius + 1):
            for z in range(coord[2] - radius, coord[2] + radius + 1):
                if hex_coord_available((x, y, z), field):
                    coord_list.append((x, y, z))
    return coord_list


def __hex_circle__(coord, radius, field):
    #TODO: оптимизировать позже добавление в лист координат, сейчас лень
    """
    @param coord: cube coord of hex
    @param radius: radius in hexes
    @param field: field object
    @return: all hexes in radius steps
    """
    coord_list = []
    shift_list = []
    if not radius:
        return [coord]
    for r in range(1, radius + 1):
        shift_list.append((r, radius - r, - radius))
        for ctrl in range(6):
            x = shift_list[-1][0]
            y = shift_list[-1][1]
            shift_list.append((x + y, - x, - y))
            if hex_coord_available((x + y + coord[0], - x + coord[1], - y + coord[2]), field):
                coord_list.append((x + y + coord[0], - x + coord[1], - y + coord[2]))
    return coord_list


def __hex_angle__(coord1, coord2):
    #TODO: попробовать убрать второй elif
    """
    @param coord1: cube coord of first hex
    @param coord2: cube coord of second hex
    @return: line angle between two hexes
    """
    if coord2[0] == coord1[0]:
        if coord2[1] > coord1[1]:
            return 270
        return 90
    elif coord2[1] == coord1[1]:
        if coord2[0] > coord1[0]:
            return 0
        return 180
    else:
        shadow_angle = degrees(atan(abs(coord2[1] - coord1[1]) / abs(coord2[0] - coord1[0])))
        if coord2[0] > coord1[0]:
            if coord2[1] < coord1[1]:
                return shadow_angle
            return 360 - shadow_angle
        elif coord2[1] < coord1[1]:
            return 180 - shadow_angle
        return shadow_angle + 180


def _shadow_optimize_(shadows):
    #TODO: вставить в проверку видимости
    shadows.sort(key=itemgetter(0))
    for ctrl in range(len(shadows) - 1):
        while True:
            if ctrl < len(shadows) - 1:
                if shadows[ctrl][1] >= shadows[ctrl + 1][0]:
                    if shadows[ctrl][1] < shadows[ctrl + 1][1]:
                        shadows[ctrl][1] = shadows[ctrl + 1][1]
                    shadows[ctrl + 1:len(shadows) - 1] = shadows[ctrl + 2:len(shadows)]
                    del shadows[-1]
                else:
                    break
            else:
                return shadows
    return shadows


def hexagon_visible(shadows, hexagon, field):
    #TODO: вставить в проверку видимости
    status = True
    if shadows:
        for shadow in shadows:
            if hexagon[1] > shadow[0] and hexagon[2] < shadow[1]:
                return
            if shadow[0] < hexagon[3] < shadow[1]:
                status = False
    if status:
        coord_offset = hex_cube_to_offset(hexagon[0])
        field.map[coord_offset[0]][coord_offset[1]][1].visible_change(2)
    else:
        coord_offset = hex_cube_to_offset(hexagon[0])
        field.map[coord_offset[0]][coord_offset[1]][1].visible_change(1)


def hex_visible_true(field, coord, radius):
    #TODO: если непрозрачен текущий
    """
    @param field: field object to find map size
    @param coord: cube coord of viewer position
    @param radius: ability to see far
    """
    angles = [(0.25, 0), (0.75, 0), (1, sqrt(3) / 4), (0.75, sqrt(3) / 2), (0.25, sqrt(3) / 2), (0, sqrt(3) / 4)]
    shadows = []
    coord_offset = hex_cube_to_offset(coord)
    field.map[coord_offset[0]][coord_offset[1]][1].visible_change(2)
    logic_coord1 = __hex_to_coord__(coord, (0.5, sqrt(3) / 4))
    for r in range(1, radius + 1):
        temp_shadows = __hex_circle__(coord, r - 1, field)
        for temp_shadow in temp_shadows:
            coord_offset = hex_cube_to_offset(temp_shadow)
            if not field.map[coord_offset[0]][coord_offset[1]][1].transparency:
                shadow_angles = []
                for angle in angles:
                    logic_coord2 = __hex_to_coord__(temp_shadow, angle)
                    shadow_angles.append(round(__hex_angle__(logic_coord1, logic_coord2), 0))
                max_angle = max(shadow_angles)
                min_angle = min(shadow_angles)
                if max_angle - min_angle > 180:
                    min_angle = max([shadow_angle for shadow_angle in shadow_angles if shadow_angle < 180])
                    max_angle = min([shadow_angle for shadow_angle in shadow_angles if shadow_angle > 180])
                    shadows.append(list((max_angle, min_angle + 360)))
                    shadows.append(list((max_angle - 360, min_angle)))
                else:
                    shadows.append(list((min_angle, max_angle)))
                    shadows.append(list((min_angle - 360, max_angle - 360)))
        hexes_coord = __hex_circle__(coord, r, field)
        hexes = []
        for temp_hex in hexes_coord:
            hex_angles = []
            for angle in angles:
                logic_coord2 = __hex_to_coord__(temp_hex, angle)
                hex_angles.append(round(__hex_angle__(logic_coord1, logic_coord2), 0))
            max_angle = max(hex_angles)
            min_angle = min(hex_angles)
            center_angle = round(__hex_angle__(logic_coord1, __hex_to_coord__(temp_hex, (0.5, sqrt(3) / 4))), 0)
            if max_angle - min_angle > 180:
                min_angle = max([shadow_angle for shadow_angle in hex_angles if shadow_angle < 180])
                max_angle = min([shadow_angle for shadow_angle in hex_angles if shadow_angle > 180])
                hexes.append((temp_hex, max_angle - 360, min_angle, center_angle))
            else:
                hexes.append((temp_hex, min_angle, max_angle, center_angle))
        _shadow_optimize_(shadows)
        for hexagon in hexes:
            hexagon_visible(shadows, hexagon, field)


def hex_visible_false(field, coord, radius):
    """
    @param field: field object to find map size
    @param coord: cube coord of viewer position
    @param radius: ability to see far
    """
    for x in range(coord[0] - radius, coord[0] + radius + 1):
        for y in range(coord[1] - radius, coord[1] + radius + 1):
            for z in range(coord[2] - radius, coord[2] + radius + 1):
                if hex_coord_available((x, y, z), field):
                    coord_offset = hex_cube_to_offset((x, y))
                    field.map[coord_offset[0]][coord_offset[1]][1].visibility = False


def path_finding(start_coord, finish_coord, field, avoid):
    #(coord, F, G finish, H start, L, parent)
    """
    @param start_coord: start hex cube coord
    @param finish_coord: goal hex cube coord
    @param field: field object
    @param avoid: hexes to avoid in path finding
    @return: path between two hexes
    """
    open_list = [(finish_coord, hex_distance(start_coord, finish_coord), 0,
                  hex_distance(start_coord, finish_coord), __line_length__(start_coord, finish_coord), False)]
    open_coord = [finish_coord]
    close_list = []
    close_coord = []
    for mob in avoid:
        for coord in __hex_radius__(mob.coord, 1, field):
            close_coord.append(coord)
    while open_list:
        work_coord = min(open_list, key=itemgetter(1, 4))
        close_list.append(work_coord)
        if work_coord[0] == start_coord:
            finally_list = [close_list[-1][0]]
            x = close_list[-1]
            while x[5]:
                finally_list.append(x[5])
                for y in close_list:
                    if y[0] == x[5]:
                        x = y
                        break
            return finally_list[1:]
        close_coord.append(work_coord[0])
        open_coord.remove(work_coord[0])
        open_list.remove(work_coord)
        for neigh_coord in __hex_neighbours__(work_coord[0]):
            offset_coord = hex_cube_to_offset(neigh_coord)
            if (field.map[offset_coord[0]][offset_coord[1]][1].passability_change or
                    field.map[offset_coord[0]][offset_coord[1]][
                        1].passability) and not neigh_coord in close_coord and not neigh_coord in open_coord:
                g = work_coord[2] + 1
                h = hex_distance(start_coord, neigh_coord)
                open_list.append((neigh_coord, g + h, g, h, __line_length__(start_coord, neigh_coord), work_coord[0]))
                open_coord.append(neigh_coord)
    return []


def ex_path_finding(start_coord, finish_coord, field, avoid):
    #(coord, F, G finish, H start, L, parent)
    """
    @param start_coord: start hex cube coord
    @param finish_coord: goal hex cube coord
    @param field: field object
    @param avoid: hexes to avoid in path finding
    @return: path between two hexes
    """
    open_list = [(finish_coord, hex_distance(start_coord, finish_coord), 0,
                  hex_distance(start_coord, finish_coord), __line_length__(start_coord, finish_coord), False)]
    open_coord = [finish_coord]
    close_list = []
    close_coord = []
    for mob in avoid:
        for coord in __hex_radius__(mob.coord, 1, field):
            close_coord.append(coord)
    while open_list:
        work_coord = min(open_list, key=itemgetter(1, 4))
        close_list.append(work_coord)
        close_coord.append(work_coord[0])
        open_coord.remove(work_coord[0])
        open_list.remove(work_coord)
        for neigh_coord in __hex_neighbours__(work_coord[0]):
            if neigh_coord == start_coord:
                g = work_coord[2] + 1
                h = hex_distance(start_coord, neigh_coord)
                close_list.append((neigh_coord, g + h, g, h, __line_length__(start_coord, neigh_coord), work_coord[0]))
                finally_list = [close_list[-1][0]]
                x = close_list[-1]
                while x[5]:
                    finally_list.append(x[5])
                    for y in close_list:
                        if y[0] == x[5]:
                            x = y
                            break
                return finally_list[1:]
            if not hex_coord_available(neigh_coord, field):
                continue
            offset_coord = hex_cube_to_offset(neigh_coord)
            if (field.map[offset_coord[0]][offset_coord[1]][1].passability_change or
                    field.map[offset_coord[0]][offset_coord[1]][
                        1].passability) and not neigh_coord in close_coord and not neigh_coord in open_coord:
                g = work_coord[2] + 1
                h = hex_distance(start_coord, neigh_coord)
                open_list.append((neigh_coord, g + h, g, h, __line_length__(start_coord, neigh_coord), work_coord[0]))
                open_coord.append(neigh_coord)
    return []


def neighbour_finding(start_coord, field, avoid):
    #(coord, G start)
    """
    @param start_coord: start hex cube coord
    @param field: field object
    @param avoid: hexes to avoid in neigh finding
    @return: most close neighbour
    """
    open_list = [(start_coord, 0)]
    open_coord = [start_coord]
    close_list = []
    close_coord = []
    coord = list(field.objects.keys())
    while open_list:
        work_coord = min(open_list, key=itemgetter(1))
        close_list.append(work_coord)
        if work_coord[0] in coord and work_coord[0] != start_coord:
            if not field.objects[work_coord[0]] in avoid:
                return field.objects[work_coord[0]]
        close_coord.append(work_coord[0])
        open_coord.remove(work_coord[0])
        open_list.remove(work_coord)
        for neigh_coord in __hex_neighbours__(work_coord[0]):
            offset_coord = hex_cube_to_offset(neigh_coord)
            if (field.map[offset_coord[0]][offset_coord[1]][1].passability_change or
                    field.map[offset_coord[0]][offset_coord[1]][
                        1].passability) and not neigh_coord in close_coord and not neigh_coord in open_coord:
                open_list.append((neigh_coord, work_coord[1] + 1))
                open_coord.append(neigh_coord)
    return False


def unexplored_finding(start_coord, field, avoid):
    #(coord, G start)
    """
    @param start_coord: start hex cube coord
    @param field: field object
    @param avoid: hexes to avoid in neigh finding
    @return: most close neighbour
    """
    open_list = [(start_coord, 0)]
    open_coord = [start_coord]
    close_list = []
    close_coord = []
    while open_list:
        work_coord = min(open_list, key=itemgetter(1))
        close_list.append(work_coord)
        close_coord.append(work_coord[0])
        open_coord.remove(work_coord[0])
        open_list.remove(work_coord)
        for neigh_coord in __hex_neighbours__(work_coord[0]):
            offset_coord = hex_cube_to_offset(neigh_coord)
            if not field.map[offset_coord[0]][offset_coord[1]][1].exploration:
                return neigh_coord
            if (field.map[offset_coord[0]][offset_coord[1]][1].passability_change or
                    field.map[offset_coord[0]][offset_coord[1]][
                        1].passability) and not neigh_coord in close_coord and not neigh_coord in open_coord:
                open_list.append((neigh_coord, work_coord[1] + 1))
                open_coord.append(neigh_coord)
    return False


def neighbours_in_radius(coord, radius, field):
    """
    @param coord: start hex cube coord
    @param field: field object
    @param radius: radius to find neighbours
    @return: all neighbours in radius
    """
    hexagons = __hex_radius__(coord, radius, field)
    neighbours = []
    for hexagon in hexagons:
        if hexagon in field.objects and hexagon != coord:
            neighbours.append(field.objects[hexagon])
    return neighbours
