from pygame.time import get_ticks
from states.Communication import Communication


class Attacking(Communication):
    def __init__(self, mob, aggressor):
        Communication.__init__(self, mob)
        self.aggressor = aggressor
        self.kick = get_ticks()

    def update(self, field):
        if get_ticks() - self.kick >= self.mob.stats.kick_time:
            self.aggressor.health -= 1
            if self.aggressor.health <= 0:
                self.aggressor.alive = False
            self.kick = get_ticks()
        return True

    def check(self, field):
        if not self.aggressor.alive:
            return 7
        return True
