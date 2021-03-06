class File():
    def __init__(self, name):
        try:
            file = open('res/' + name)
            self.info = file.readlines()
        except IOError:
            from bin.Worker import error_message
            error_message("Loading:", "not found " + name)

    def get_info(self, string):
        return self.info[string].split(" ")
