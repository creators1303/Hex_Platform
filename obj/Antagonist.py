from st.PrimaryAntagonist import PrimaryAntagonist
from obj.Existence import Existence
from obj.Stats import Stats


class Antagonist(Existence):

    def __init__(self, coord):
        Existence.__init__(self, coord, PrimaryAntagonist(self))
        self.stats = Stats(self)

    @staticmethod
    def status_change():
        pass

    def virtual_image_name(self):
        return self.__class__.__name__ + '/' + 'self', 255
