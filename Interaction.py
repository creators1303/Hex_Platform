from pygame.constants import KEYDOWN, K_UP, K_DOWN, K_RETURN
from pygame.event import poll, clear
from Graphic import Menu


def pause_menu(screen):
    menu = Menu(("Continue", "Quit"), screen, 120)
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
                    return True
                if choose == 1:
                    return False
        clear()