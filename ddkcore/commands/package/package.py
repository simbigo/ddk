from ddkcore.command import Command
from ddkcore.commands.package.install import InstallCommand
from ddkcore.commands.package.remove import RemoveCommand
from ddkcore.commands.package.update import UpdateCommand


class PackageCommand(Command):

    def configure(self):
        description = "Package management."
        self.set_description(description)
        self.set_title("Available actions")
        self.set_usage(
            self.get_kit().get_name() +
            " [options...] " +
            self.get_name() +
            " <action> ...\n\n" +
            description
        )

        self.add_sub_command(InstallCommand())
        self.add_sub_command(RemoveCommand())
        self.add_sub_command(UpdateCommand())

    def get_name(self):
        return "package"
