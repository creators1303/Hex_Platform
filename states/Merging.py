from pygame.time import get_ticks
from states.Communication import Communication


class Merging(Communication):
    def __init__(self, mob, merger):
        Communication.__init__(self, mob, merger)
        self.merge = get_ticks()

    def update(self, field):
        if get_ticks() - self.merge >= self.mob.stats.merge_time:
            status = self.main_merger()
            if status == 1:
                self.mob.health += 1
                self.communication.health -= 1
            elif status == 0:
                self.mob.health -= 1
                self.communication.health += 1
            self.merge = get_ticks()
        return True

    def main_merger(self):
        if self.communication.current_state.__class__.__name__ != "Merging":
            return 0
        if self.communication.current_state.communication != self.mob:
            return 0
        if self.mob.health >= self.communication.health > 0:
            return 1
        return -1


    def check(self, field):
        return True
