class Stats():
    def __init__(self, obj):
        from json import load
        file = open("res/" + obj.__class__.__name__ + "/" + "SKILLS.json")
        info = load(file)
        self.view_radius = info["view_radius"]
        self.step_time = info["step_time"]
        self.kick_time = info["kick_time"]
        self.merge_time = info["merge_time"]
        self.find_time = info["find_time"]
        self.despawn_time = info["despawn_time"]
        self.path_time = info["path_time"]
        file = open("res/" + obj.__class__.__name__ + "/" + "RELATIONSHIPS.json")
        self.relationships = load(file)