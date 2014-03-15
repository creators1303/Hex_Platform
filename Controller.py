def process(screen, field):
    from Graphic import ImageStorage
    storage = ImageStorage()

    while True:
        for supervisor in field.supervisors:
            if not supervisor.state_update(field):
                return

        objects = list(field.objects.values())
        any(obj.state_update(field) for obj in objects)
        any(obj.state_check(field) for obj in objects)
        any(obj.alive_check(field) for obj in objects)

        field.camera.draw_field(screen, field, storage)