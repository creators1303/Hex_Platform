from pygame.time import get_ticks
from states.Main import Main


class Attacking(Main):
    def __init__(self, mob, aggressor):
        Main.__init__(self, mob)
        self.aggressor = aggressor
        self.kick = get_ticks()

    def update(self, field, size):
        if get_ticks() - self.kick >= self.mob.stats.kick_time:
            self.aggressor.health -= 1
            if self.aggressor.health == 0:
                self.aggressor.alive = False
                return 2
            self.kick = get_ticks()
        return True

    def check(self, field):
        if not self.aggressor.alive:
            return 3
        return True
