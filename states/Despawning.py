from pygame.time import get_ticks
from states.Main import Main


class Despawning(Main):
    def __init__(self, mob):
        Main.__init__(self, mob)
        self.countdown = get_ticks()

    def update(self, field, size):
        if get_ticks() - self.countdown >= 3000:
            self.mob.alive = False
        return True

    def check(self, field):
        pass