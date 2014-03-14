from ctypes import cdll
from pickle import load

from pygame.display import set_mode, list_modes, set_caption
from pygame import init, quit
from pygame.constants import FULLSCREEN

from Controller import process
from objects.Field import Field

from Graphic import Menu


def start_menu():
    init()
    screen = set_mode(list_modes()[0], FULLSCREEN)
    set_caption("Hero Misadventures")
    menu = Menu(("Previous Field", "New Field", "Load Field", "Quit"), screen)
    while True:
        choose = menu.update()
        if choose == 0:
            field = Field(screen)
            process(screen, field)
        elif choose == 1:
            cdll.LoadLibrary("Generator.dll").main_generator()
            field = Field(screen)
            process(screen, field)
        elif choose == 2:
            field = load(open("resources/SAVE.HMsave", "rb"))
            field.screen = screen
            process(screen, field)
        elif choose == 3:
            return
    quit()


def main():
    start_menu()

if __name__ == "__main__":
    #import cProfile
    #import pstats
    #cProfile.run("main()", 'testing/profile.txt')
    #p = pstats.Stats('testing/profile.txt')
    #p.sort_stats('time')
    #p.print_stats()
    main()