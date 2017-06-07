from argparse import ArgumentParser


class DdkParser(ArgumentParser):

    def __init__(self, **kwargs):
        super(DdkParser, self).__init__(**kwargs)

        self._optionals.title = "Options"
