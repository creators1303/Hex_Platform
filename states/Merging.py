from pygame.time import get_ticks
from states.Communication import Communication


class Merging(Communication):
    def __init__(self, mob, merger):
        Communication.__init__(self, mob)
        self.merger = merger
        self.merge = get_ticks()

    def update(self, field):
        if get_ticks() - self.merge >= self.mob.stats.merge_time:
            if self.mob.health >= self.merger.health > 0:
                self.mob.health += 1
                self.merger.health -= 1
                if self.merger.health <= 0:
                    self.merger.alive = False
            self.merge = get_ticks()
        return True

    def check(self, field):
        if not self.merger.alive:
            return 2
        return True
