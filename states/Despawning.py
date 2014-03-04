from pygame.time import get_ticks
from states.Alone import Alone


class Despawning(Alone):
    def __init__(self, mob):
        Alone.__init__(self, mob)
        self.countdown = get_ticks()

    def update(self, field):
        if get_ticks() - self.countdown >= 3000:
            self.mob.alive = False
        return True

    def check(self, field):
        pass