from Graphic import ImageStorage


def process(screen, field):
    storage = ImageStorage()

    while True:
        #TODO: supervisor нормальное состояние, привязка к протагонисту
        for supervisor in field.supervisors:
            supervisor.update(field)

        objects = list(field.objects.values())
        any(obj.update(field) for obj in objects)
        any(obj.state_check(field) for obj in objects)
        any(obj.alive_check(field) for obj in objects)

        field.camera.draw_field(screen, field, storage)