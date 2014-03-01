from File import File
from Graphic import ImageStorage


def process(screen, field):
    graphic = File("GRAPHIC.HMinf")
    size = int(graphic.get_info(0)[0]), int(graphic.get_info(0)[1])

    storage = ImageStorage()

    while True:
        for dynamic_object in list(field.objects.values()):
            if not dynamic_object.update(field, size):
                return

        for dynamic_object in list(field.objects.values()):
            dynamic_object.check(field)

        field.camera.draw_field(screen, field, storage)

        if not field.objects:
            return