from ctypes import cdll
from pygame.display import set_mode, list_modes, set_caption
from pygame import init, quit
from pygame.constants import FULLSCREEN
from Controller import process
from objects.Field import Field
from pickle import load


def start_menu():
    while True:
        print("1 = new\n2 = load\n3 = quit")
        choose = int(input())
        init()
        screen = set_mode(list_modes()[0], FULLSCREEN)
        set_caption("Hero Misadventures")
        if choose == 1:
            cdll.LoadLibrary("Generator.dll").main_generator(50, 30)
            field = Field(screen)
            process(screen, field)
        if choose == 2:
            field = load(open("resources/SAVE.HMsave", "rb"))
            process(screen, field)
        if choose == 3:
            return
        quit()


def main():
    start_menu()

if __name__ == "__main__":
    #import cProfile
    #import pstats
    #cProfile.run("main()", 'filee')
    #p = pstats.Stats('filee')
    #p.sort_stats('time')
    #p.print_stats()
    main()