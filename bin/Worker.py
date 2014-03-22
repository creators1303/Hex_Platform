def object_image_load(parameters):
    """
    @param parameters: list with picture parameters (NAME, TRANSPARENCY, SIZE)
    @return: image descriptor
    """
    from pygame.constants import RLEACCEL
    from pygame import error
    from pygame.transform import scale
    import pygame.image
    try:
        image = pygame.image.load('res/' + parameters[0] + '.HMtex').convert()
    except error:
        error_message("Loading:", "not found " + parameters[0] + '.HMtex')
    else:
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        image.set_alpha(parameters[1])
        image = scale(image, (parameters[2][0], parameters[2][1]))
        return image


def error_message(exception_type, info):
    """
    @param exception_type: type of exception
    @param info: additional info about exception
    """
    from sys import exit
    print("Error in Hero Misadventures.")
    print(exception_type, info)
    exit()
