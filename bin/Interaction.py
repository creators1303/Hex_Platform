from bin.Graphic import Menu, ColorStorage
from obj.Field import Field

storage = ColorStorage()
color = storage.get_color


def admin_menu():
    from pygame.display import set_mode, list_modes, set_caption
    from pygame import init, quit

    init()
    screen = set_mode(list_modes()[0])
    set_caption("Hero Misadventures")
    menu = Menu(("Debug", "Release"), screen, text_color=color("White"), surface=color("Black"),
                selection_color=color("Slate Gray"))
    while True:
        choose = menu.update()
        if choose == -1:
            continue
        else:
            quit()
            if choose == 0:
                debug_menu()
            elif choose == 1:
                start_menu()
            return


def pause_menu(screen, field):
    menu = Menu(("Continue", "Save", "Quit"), screen, surface=color("Lime Green"),
                selection_color=color("Medium Spring Green"), text_color=color("Dodger Blue"))
    choose = menu.update()
    if choose == 0:
        return True
    if choose == 1:
        from pickle import dump

        dump(field, open("res/SAVE.HMsave", "wb"))
        return True
    if choose == 2:
        return False


def debug_menu():
    from pygame.display import set_mode, list_modes, set_caption
    from pygame import init, quit
    from bin.Controller import process

    init()
    screen = set_mode(list_modes()[0])
    set_caption("Hero Misadventures")
    menu = Menu(("Previous Field", "New Field", "Load Field", "Quit"), screen, surface=color("Firebrick"),
                text_color=color("Black"), selection_color=color("Coral"))
    while True:
        choose = menu.update()
        if choose == 0:
            field = Field(screen)
            process(screen, field)
        elif choose == 1:
            from ctypes import cdll

            cdll.LoadLibrary("Generator.dll").main_generator()
            field = Field(screen)
            process(screen, field)
        elif choose == 2:
            from pickle import load

            field = load(open("res/SAVE.HMsave", "rb"))
            field.screen = screen
            process(screen, field)
        elif choose == 3:
            quit()
            return


def start_menu():
    from pygame.display import set_mode, list_modes, set_caption
    from pygame import init, quit
    from pygame.constants import FULLSCREEN
    from bin.Controller import process
    from obj.Field import Field

    init()
    screen = set_mode(list_modes()[0], FULLSCREEN)
    set_caption("Hero Misadventures")
    menu = Menu(("Previous Field", "New Field", "Load Field", "Quit"), screen, surface=color("Lime Green"),
                selection_color=color("Medium Spring Green"), text_color=color("Dodger Blue"))
    while True:
        choose = menu.update()
        if choose == 0:
            field = Field(screen)
            process(screen, field)
        elif choose == 1:
            from ctypes import cdll

            cdll.LoadLibrary("Generator.dll").main_generator()
            field = Field(screen)
            process(screen, field)
        elif choose == 2:
            from pickle import load

            field = load(open("res/SAVE.HMsave", "rb"))
            field.screen = screen
            process(screen, field)
        elif choose == 3:
            quit()
            return