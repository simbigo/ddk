import getpass


class Console:
    COLOR_BLUE = '\033[94m'
    COLOR_GREEN = '\033[92m'
    COLOR_PURPLE = '\033[96m'
    COLOR_RED = '\033[91m'
    COLOR_VIOLET = '\033[95m'
    COLOR_YELLOW = '\033[93m'
    FORMAT_BOLD = '\033[1m'
    FORMAT_END = '\033[0m'
    FORMAT_UNDERLINE = '\033[4m'

    VERBOSITY_QUIET = -1
    VERBOSITY_SILENT = 0
    VERBOSITY_VERBOSE = 1
    VERBOSITY_DEBUG = 2

    __verbose = 0

    def __init__(self):
        pass

    def input(self, prompt=""):
        return raw_input(prompt)

    def input_password(self, prompt=""):
        return getpass.getpass(prompt)

    def output(self, text, verbosity=0, text_format=None, ):
        if self.__verbose == -1 or verbosity > self.__verbose:
            return

        if text_format is not None:
            text = text_format + text + Console.FORMAT_END
        print text

    def set_verbosity(self, value):
        self.__verbose = value
