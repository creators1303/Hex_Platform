from pygame.time import get_ticks

from states.Alone import Alone
from Logic import neighbour_finding
from states.Pursuit import Pursuit
from states.Despawning import Despawning


class Finding(Alone):
    def __init__(self, mob, avoid):
        Alone.__init__(self, mob)
        self.avoid = avoid
        self.find_time = get_ticks()

    def update(self, field):
        strike = neighbour_finding(self.mob.coord, field, self.avoid)
        if strike:
            self.mob.state = Pursuit(self.mob, strike, field)
        return True

    def check(self, field):
        if get_ticks() - self.find_time >= self.mob.stats.find_time:
            self.mob.state = Despawning(self.mob)