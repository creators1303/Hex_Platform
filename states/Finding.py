from states.Main import Main
from Logic import neighbour_finding
from states.Pursuit import Pursuit
from states.Despawning import Despawning
from pygame.time import get_ticks


class Finding(Main):
    def __init__(self, mob, avoid):
        Main.__init__(self, mob)
        self.avoid = avoid
        self.find_time = get_ticks()

    def update(self, field, size):
        strike = neighbour_finding(self.mob.coord, field, self.avoid)
        if strike:
            self.mob.state = Pursuit(self.mob, strike, field)
        return True

    def check(self, field):
        if get_ticks() - self.find_time >= self.mob.stats.find_time:
            self.mob.state = Despawning(self.mob)