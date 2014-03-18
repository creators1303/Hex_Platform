from states.Communication import Communication


class Attacking(Communication):
    def __init__(self, mob, aggressor):
        from pygame.time import get_ticks
        Communication.__init__(self, mob, aggressor)
        self.kick = get_ticks()

    def update(self, field):
        from pygame.time import get_ticks
        if get_ticks() - self.kick >= self.mob.stats.kick_time:
            self.communication.health -= 1
            self.kick = get_ticks()
        return True

    @staticmethod
    def check(field):
        return True
