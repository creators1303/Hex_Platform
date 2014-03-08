from Graphic import ImageStorage


def process(screen, field):
    storage = ImageStorage()

    while True:
        for supervisor in field.supervisors:
            supervisor.update(field)

        for dynamic_object in list(field.objects.values()):
            if not dynamic_object.update(field):
                return

        for dynamic_object in list(field.objects.values()):
            dynamic_object.state_check(field)

        for dynamic_object in list(field.objects.values()):
            dynamic_object.alive_check(field)

        field.camera.draw_field(screen, field, storage)