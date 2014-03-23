def line_length(coord1, coord2):
    """
    @param coord1: cube coord of first hex
    @param coord2: cube coord of second hex
    @return: logic length of line between first and second hexes
    """
    logic_coord1 = hex_to_coord(coord1)
    logic_coord2 = hex_to_coord(coord2)
    return ((logic_coord1[0] - logic_coord2[0]) ** 2 + (logic_coord1[1] - logic_coord2[1]) ** 2) ** 0.5


def hex_to_pixel(coord, size, field):
    """
    @param coord: cube coord of hex
    @param size: size of the image of hex
    @return: XY coord of the start drawing point
    """
    coord = coord_get_offset(coord, field)
    return list(map(int, (coord[1] * size[0] * 0.75, size[1] * (coord[0] + 0.5 * ((coord[1] + 1) % 2)))))


def hex_distance(coord1, coord2):
    """
    @param coord1: cube coord of start hex
    @param coord2: cube coord of goal hex
    @return: distance in steps between two hexes
    """
    return max([abs(coord[0] - coord[1]) for coord in zip(coord1, coord2)])


def hex_to_coord(coord, shift=(0.0, 0.0)):
    """
    @param coord: cube coord of hex
    @param shift: XY coord of shift (to angle or to center)
    @return: XY coord of the logic up-left angle of surface + shift
    """
    return coord[0] * 0.75 + shift[0], (0.5 * ((coord[0] + 1) % 2) + (coord[0] + 1) // 2 + coord[
        1]) * 0.8660254037844386 + shift[1]


def coord_get_cube(row, column):
    """
    @param row: offset row of hex
    @param column: offset column of hex
    @return: cube coord of hex
    """
    x = column
    y = row - (column + column % 2) // 2
    return x, y, -x - y


def coord_get_offset(coord, field):
    """
    @param coord: cube coord of hex
    @return: offset coord of hex
    """
    return field.coord_dict[coord]


def hex_neighbours(coord, field):
    """
    @param coord: cube coord of hex
    @return: cube coord of neighbours
    """
    return [tuple([sum(temp) for temp in zip(each, coord)]) for each in field.neighbours_list]


def pixel_to_hex(coord, size, field):
    """
    @param coord: XY coord of point
    @return: cube coord of hex
    """
    x_coord = coord[0] / size[0]
    y_coord = coord[1] / size[1]
    coord = x_coord, y_coord
    x = int(x_coord / 0.75)
    y = int(y_coord - (x + 1) % 2 * 0.4330127018922193)
    hexagon = field.map[y][x][0]
    logic_coord1 = hex_to_coord(hexagon, (0.5, 0.4330127018922193))
    logic_coord2 = hex_to_coord((hexagon[0] - 1, hexagon[1], hexagon[2] + 1), (0.5, 0.4330127018922193))
    logic_coord3 = hex_to_coord((hexagon[0] - 1, hexagon[1] + 1, hexagon[2]), (0.5, 0.4330127018922193))
    line1 = line_length(coord, logic_coord1)
    line2 = line_length(coord, logic_coord2)
    line3 = line_length(coord, logic_coord3)
    if line3 > line1 < line2:
        return hexagon
    if line3 > line2 < line1:
        return hexagon[0] - 1, hexagon[1], hexagon[2] + 1
    return hexagon[0] - 1, hexagon[1] + 1, hexagon[2]


def coord_available(coord, field):
    """
    @param coord: cube coord of hex
    @param field: field object to find map size
    @return: (True) if there exists hex with this coord, else (False)
    """
    return coord in field.coord_dict.keys()


def hex_radius(coord, radius, field):
    """
    @param coord: cube coord of hex
    @param radius: radius in hexes
    @param field: field object
    @return: all hexes in radius
    """
    coord_list = []
    for each in field.radius_dict[str(radius)]:
        current = tuple([sum(temp) for temp in zip(each, coord)])
        if coord_available(current, field):
            coord_list.append(current)
    return coord_list


def hex_circle(coord, radius, field):
    """
    @param coord: cube coord of hex
    @param radius: radius in hexes
    @param field: field object
    @return: all hexes in radius steps
    """
    if radius == -1:
        return []
    coord_list = []
    for each in field.circles_dict[str(radius)]:
        current = tuple([sum(temp) for temp in zip(each, coord)])
        if coord_available(current, field):
            coord_list.append(current)
    return coord_list


def __hex_angle__(coord1, coord2):
    """
    @param coord1: cube coord of first hex
    @param coord2: cube coord of second hex
    @return: line angle between two hexes
    """
    from math import degrees, atan

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


def hexagon_visible(shadows, hexagon, field):
    status = True
    for shadow in shadows:
        if hexagon[1] > shadow[0] and hexagon[2] < shadow[1]:
            return
        if shadow[0] < hexagon[3] < shadow[1]:
            status = False
    coord_offset = coord_get_offset(hexagon[0], field)
    if status:
        field.map[coord_offset[0]][coord_offset[1]][1].visible_change(2)
    else:
        if field.map[coord_offset[0]][coord_offset[1]][1].visibility != 2:
            field.map[coord_offset[0]][coord_offset[1]][1].visible_change(1)


def hex_visible_true(field, coord, radius):
    """
    @param field: field object to find map size
    @param coord: cube coord of viewer position
    @param radius: ability to see far
    """
    shadows = []
    for r in range(radius + 1):
        temp_shadows = hex_circle(coord, r - 1, field)
        for temp_shadow in temp_shadows:
            coord_offset = coord_get_offset(temp_shadow, field)
            if not field.map[coord_offset[0]][coord_offset[1]][1].transparency:
                shadows.extend(field.shadows_dict[str(r - 1)][
                    str((coord[0] - temp_shadow[0], coord[1] - temp_shadow[1], coord[2] - temp_shadow[2]))])
        hexes_coord = hex_circle(coord, r, field)
        hexes = []
        for temp_hex in hexes_coord:
            current = list([temp_hex])
            current.extend(field.hexes_dict[str(r)][str((coord[0] - temp_hex[0], coord[1] - temp_hex[1], coord[2] - temp_hex[2]))])
            hexes.append(current)
        shadows.sort()
        ctrl = 0
        while ctrl < len(shadows) - 1:
            if shadows[ctrl][1] >= shadows[ctrl + 1][0]:
                if shadows[ctrl][1] < shadows[ctrl + 1][1]:
                    shadows[ctrl][1] = shadows[ctrl + 1][1]
                del shadows[ctrl + 1]
                ctrl -= 1
            ctrl += 1
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
            z = - x - y
            if coord_available((x, y, z), field) and abs(z - coord[2]) <= radius:
                coord_offset = coord_get_offset((x, y, -x - y), field)
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
    from operator import itemgetter

    open_list = [(finish_coord, hex_distance(start_coord, finish_coord), 0,
                  hex_distance(start_coord, finish_coord), line_length(start_coord, finish_coord), False)]
    open_coord = [finish_coord]
    close_list = []
    close_coord = []
    for mob in avoid:
        for coord in hex_radius(mob.coord, 2, field):
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
        for neigh_coord in hex_neighbours(work_coord[0], field):
            offset_coord = coord_get_offset(neigh_coord, field)
            if (field.map[offset_coord[0]][offset_coord[1]][1].passability_change or
                    field.map[offset_coord[0]][offset_coord[1]][
                        1].passability) and not neigh_coord in close_coord and not neigh_coord in open_coord:
                g = work_coord[2] + 1
                h = hex_distance(start_coord, neigh_coord)
                open_list.append(
                    (neigh_coord, g + h, g, h, line_length(start_coord, neigh_coord), work_coord[0]))
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
    from operator import itemgetter

    open_list = [(finish_coord, hex_distance(start_coord, finish_coord), 0,
                  hex_distance(start_coord, finish_coord), line_length(start_coord, finish_coord), False)]
    open_coord = [finish_coord]
    close_list = []
    close_coord = []
    for mob in avoid:
        for coord in hex_radius(mob.coord, 1, field):
            close_coord.append(coord)
    while open_list:
        work_coord = min(open_list, key=itemgetter(1, 4))
        close_list.append(work_coord)
        close_coord.append(work_coord[0])
        open_coord.remove(work_coord[0])
        open_list.remove(work_coord)
        for neigh_coord in hex_neighbours(work_coord[0], field):
            if neigh_coord == start_coord:
                return work_coord[0]
            if not coord_available(neigh_coord, field):
                continue
            offset_coord = coord_get_offset(neigh_coord, field)
            if (field.map[offset_coord[0]][offset_coord[1]][1].passability_change or
                    field.map[offset_coord[0]][offset_coord[1]][
                        1].passability) and not neigh_coord in close_coord and not neigh_coord in open_coord:
                g = work_coord[2] + 1
                h = hex_distance(start_coord, neigh_coord)
                open_list.append(
                    (neigh_coord, g + h, g, h, line_length(start_coord, neigh_coord), work_coord[0]))
                open_coord.append(neigh_coord)
    return False


def neighbour_finding(start_coord, field, avoid):
    #(coord, G start)
    """
    @param start_coord: start hex cube coord
    @param field: field object
    @param avoid: hexes to avoid in neigh finding
    @return: most close neighbour
    """
    from operator import itemgetter

    open_list = [(start_coord, 0)]
    open_coord = [start_coord]
    close_list = []
    close_coord = []
    coordinates = list(field.objects.keys())
    for mob in avoid:
        for coord in hex_radius(mob.coord, 2, field):
            close_coord.append(coord)
    if len(avoid) == len(coordinates) - 1:
        return False
    while open_list:
        work_coord = min(open_list, key=itemgetter(1))
        close_list.append(work_coord)
        if work_coord[0] in coordinates and work_coord[0] != start_coord:
            return field.objects[work_coord[0]]
        close_coord.append(work_coord[0])
        open_coord.remove(work_coord[0])
        open_list.remove(work_coord)
        for neigh_coord in hex_neighbours(work_coord[0], field):
            offset_coord = coord_get_offset(neigh_coord, field)
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
    from operator import itemgetter

    open_list = [(start_coord, 0)]
    open_coord = [start_coord]
    close_list = []
    close_coord = []
    for mob in avoid:
        for coord in hex_radius(mob.coord, 2, field):
            close_coord.append(coord)
    while open_list:
        work_coord = min(open_list, key=itemgetter(1))
        close_list.append(work_coord)
        close_coord.append(work_coord[0])
        open_coord.remove(work_coord[0])
        open_list.remove(work_coord)
        for neigh_coord in hex_neighbours(work_coord[0], field):
            if not neigh_coord in close_coord:
                offset_coord = coord_get_offset(neigh_coord, field)
                if not field.map[offset_coord[0]][offset_coord[1]][1].exploration:
                    return neigh_coord
                if (field.map[offset_coord[0]][offset_coord[1]][1].passability_change or
                        field.map[offset_coord[0]][offset_coord[1]][
                            1].passability) and not neigh_coord in open_coord:
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
    hexagons = hex_radius(coord, radius, field)
    neighbours = []
    for hexagon in hexagons:
        if hexagon in field.objects and hexagon != coord:
            neighbours.append(field.objects[hexagon])
    return neighbours
