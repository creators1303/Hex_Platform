import sys

import pygame
from pygame.constants import RLEACCEL


def object_image_load(parameters):
    """
    @param parameters: list with picture parameters (NAME, TRANSPARENCY, SIZE)
    @return: image descriptor
    """
    try:
        image = pygame.image.load('resources/' + parameters[0] + '.HMtex').convert()
    except pygame.error:
        error_message("Loading:", "not found " + parameters[0] + '.HMtex')
    else:
        image.set_colorkey(image.get_at((0, 0)), RLEACCEL)
        image.set_alpha(parameters[1])
        image = pygame.transform.scale(image, (parameters[2][0], parameters[2][1]))
        return image


def error_message(exception_type, info):
    """
    @param exception_type: type of exception
    @param info: additional info about exception
    """
    print("Error in Hero Misadventures.")
    print(exception_type, info)
    sys.exit()
