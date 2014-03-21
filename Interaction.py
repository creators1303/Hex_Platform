from Graphic import Menu


def pause_menu(screen, field):
    menu = Menu(("Continue", "Save", "Quit"), screen)
    choose = menu.update()
    if choose == 0:
        return True
    if choose == 1:
        from pickle import dump
        dump(field, open("resources/SAVE.HMsave", "wb"))
        return True
    if choose == 2:
        return False


def start_menu():
    from pygame.display import set_mode, list_modes, set_caption
    from pygame import init, quit
    from pygame.constants import FULLSCREEN
    from Controller import process
    from objects.Field import Field
    init()
    screen = set_mode(list_modes()[0])#, FULLSCREEN)
    set_caption("Hero Misadventures")
    menu = Menu(("Previous Field", "New Field", "Load Field", "Quit"), screen)
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
            field = load(open("resources/SAVE.HMsave", "rb"))
            field.screen = screen
            process(screen, field)
        elif choose == 3:
            return
    quit()