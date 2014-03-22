def process(screen, field):
    from bin.Graphic import ImageStorage
    storage = ImageStorage()

    while True:
        if not any(obj.state_update(field) for obj in field.supervisors):
            return

        objects = list(field.objects.values())
        any(obj.state_update(field) for obj in objects)
        any(obj.state_check(field) for obj in objects)
        any(obj.alive_check(field) for obj in objects)

        field.camera.draw_field(screen, field, storage)