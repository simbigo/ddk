from abc import ABCMeta, abstractmethod


class Command:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.__kit = None
        self.__sub_commands = {}
        self.__subparsers = None
        self._parent_command = None
        self.description = ""
        self.title = ""
        self.usage = ""

    def add_sub_command(self, command):
        self.__sub_commands[command.get_name()] = command
        command.set_kit(self.get_kit())
        command._parent_command = self

    def configure(self):
        pass

    def configure_parser(self, parser):
        pass

    def configure_sub_commands(self, parser):
        for cmd_name in self.__sub_commands.keys():
            command = self.__sub_commands[cmd_name]
            command.configure()
            if self.__subparsers is None:
                self.__subparsers = parser.add_subparsers(dest=cmd_name, metavar="", title=self.title)

            parser_config = dict(help=command.description, add_help=False, conflict_handler="resolve")
            command_parser = self.__subparsers.add_parser(cmd_name, **parser_config)
            self.get_kit().add_default_arguments(command_parser)
            command.configure_parser(command_parser)
            command_parser.set_defaults(cmd_callback=command)

            if len(command.usage) > 0:
                command_parser.usage = command.usage

    def get_kit(self):
        return self.__kit

    @abstractmethod
    def get_name(self):
        """Command name"""

    def has_sub_commands(self):
        return len(self.__sub_commands) > 0

    def run(self, args, terminal):
        pass

    def set_description(self, description):
        self.description = description
        return self

    def set_kit(self, kit):
        """Set application instance"""
        self.__kit = kit
        return self

    def set_title(self, title):
        self.title = title
        return self

    def set_usage(self, usage):
        self.usage = usage
        return self
