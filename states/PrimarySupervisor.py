from states.Alone import Alone


class PrimarySupervisor(Alone):
    def __init__(self, mob):
        Alone.__init__(self, mob)

    def update(self, field):
        from Graphic import Viewer
        field.camera = Viewer()
        return True

    @staticmethod
    def check(field):
        return 7