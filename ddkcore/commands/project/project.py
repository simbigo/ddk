from ddkcore.command import Command
from ddkcore.commands.project.get import GetCommand
from ddkcore.commands.project.init import InitCommand
from ddkcore.commands.project.list import ListCommand


class ProjectCommand(Command):

    def configure(self):
        description = "Management your projects."
        self.set_description(description)
        self.set_title("Available actions")
        self.set_usage(
            self.get_kit().get_name() +
            " [options...] " +
            self.get_name() +
            " <action> ...\n\n" +
            description
        )

        self.add_sub_command(GetCommand())
        self.add_sub_command(InitCommand())
        self.add_sub_command(ListCommand())

    def get_name(self):
        return "project"
