from ddkcore.command import Command


class VersionCommand(Command):

    def configure(self):
        description = "Show ddk version."
        self.set_description(description)
        self.set_usage(self.get_kit().get_name() + " " + self.get_name() + " [options...]\n\n" + description)

    def get_name(self):
        return 'version'

    def run(self, args, terminal):
        terminal.output(self.get_kit().get_version())
