class File():
    def __init__(self, name):
        try:
            self.file = open('resources/' + name)
            self.info = self.file.readlines()
        except IOError:
            from Worker import error_message
            error_message("Loading:", "not found " + name)

    def get_info(self, string):
        return self.info[string].split(" ")
