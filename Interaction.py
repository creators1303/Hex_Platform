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