from st.Alone import Alone


class Despawning(Alone):
    def __init__(self, mob):
        Alone.__init__(self, mob)
        from pygame.time import get_ticks
        self.countdown = get_ticks()

    def update(self, field):
        from pygame.time import get_ticks
        if get_ticks() - self.countdown >= self.mob.stats.despawn_time:
            self.mob.health = 0
        return True

    @staticmethod
    def check(field):
        return True