from File import File


class Stats():
    def __init__(self, obj):
        skills = File(obj.__class__.__name__ + '/' + "SKILLS.HMinf")
        relationships = File(obj.__class__.__name__ + '/' + "RELATIONSHIPS.HMinf")
        skills_dict = {}
        for string in skills.info:
            string = string.split(" ")
            skills_dict[string[0]] = int(string[1])
        self.view_radius = skills_dict["view_radius"]
        self.step_time = skills_dict["step_time"]
        self.kick_time = skills_dict["kick_time"]
        self.merge_time = skills_dict["merge_time"]
        self.find_time = skills_dict["find_time"]

        self.relationships = {}
        for string in relationships.info:
            string = string.split(" ")
            self.relationships[string[0]] = string[1].rstrip('\n')
        pass