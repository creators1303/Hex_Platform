from ctypes import cdll
from pickle import load

from pygame.display import set_mode, list_modes, set_caption
from pygame import init, quit
from pygame.constants import FULLSCREEN

from Controller import process
from objects.Field import Field
from objects.Supervisor import Supervisor


def start_menu():
    while True:
        print("1 = new\n2 = load\n3 = quit")
        choose = int(input())
        init()
        screen = set_mode(list_modes()[0], FULLSCREEN)
        set_caption("Hero Misadventures")
        if choose == 1:
            cdll.LoadLibrary("Generator.dll").main_generator(50, 40)
            field = Field(screen)
            field.supervisors.append(Supervisor())
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
    #cProfile.run("main()", 'testing/profile.txt')
    #p = pstats.Stats('testing/profile.txt')
    #p.sort_stats('cumulative')
    #p.print_stats()
    main()