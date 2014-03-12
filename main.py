from ctypes import cdll
from pickle import load

from pygame.display import set_mode, list_modes, set_caption
from pygame import init, quit
from pygame.constants import FULLSCREEN, KEYDOWN, K_UP, K_DOWN, K_RETURN
from pygame.event import poll, clear

from Controller import process
from objects.Field import Field

from Graphic import Menu


def start_menu():
    init()
    screen = set_mode(list_modes()[0])#, FULLSCREEN)
    set_caption("Hero Misadventures")
    menu = Menu(("New Field", "Load Field", "Quit"), screen, 120)
    while True:
        menu.draw(0)
        event = poll()
        if event.type == KEYDOWN:
            if event.key == K_UP:
                menu.draw(-1)
            if event.key == K_DOWN:
                menu.draw(1)
            if event.key == K_RETURN:
                choose = menu.get_position()
                if choose == 0:
                    #cdll.LoadLibrary("Generator.dll").main_generator(50, 50)
                    field = Field(screen)
                    process(screen, field)
                if choose == 1:
                    field = load(open("resources/SAVE.HMsave", "rb"))
                    process(screen, field)
                if choose == 2:
                    return
        clear()
    quit()


def main():
    start_menu()

if __name__ == "__main__":
    '''import cProfile
    import pstats
    cProfile.run("main()", 'testing/profile.txt')
    p = pstats.Stats('testing/profile.txt')
    p.sort_stats('cumulative')
    p.print_stats()'''
    main()