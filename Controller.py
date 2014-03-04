from Graphic import ImageStorage


def process(screen, field):
    storage = ImageStorage()

    while True:
        for dynamic_object in list(field.objects.values()):
            if not dynamic_object.update(field):
                return

        for dynamic_object in list(field.objects.values()):
            dynamic_object.check(field)

        field.camera.draw_field(screen, field, storage)

        if not field.objects:
            return