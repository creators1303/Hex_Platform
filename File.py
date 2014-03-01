from Worker import error_message


class File():
    #TODO: заменить на исключение
    def __init__(self, name):
        self.info = False
        try:
            file = open('resources/' + name)
            self.info = file.readlines()
        except IOError:
            error_message("Loading:", "not found " + name)

    def get_info(self, string):
        return self.info[string].split(" ")
