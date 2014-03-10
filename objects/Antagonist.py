from objects.Existence import Existence


class Antagonist(Existence):

    def __init__(self, coord):
        from objects.Stats import Stats
        from states.PrimaryAntagonist import PrimaryAntagonist
        Existence.__init__(self, coord, PrimaryAntagonist(self))
        self.stats = Stats(self)

    @staticmethod
    def status_change():
        pass

    def virtual_image_name(self):
        return self.__class__.__name__ + '/' + 'self', 255
