from pygame.time import get_ticks
from states.Communication import Communication


class Merging(Communication):
    def __init__(self, mob, merger):
        Communication.__init__(self, mob)
        self.communication = merger
        self.merge = get_ticks()

    def update(self, field):
        if get_ticks() - self.merge >= self.mob.stats.merge_time:
            if self.mob.health >= self.communication.health > 0:
                self.mob.health += 1
                self.communication.health -= 1
            self.merge = get_ticks()
        return True

    def check(self, field):
        return True
