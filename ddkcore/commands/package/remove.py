from ddkcore.command import Command


class RemoveCommand(Command):

    def configure(self):
        description = "Remove ddk package."
        self.set_description(description)
        self.set_usage(
            self.get_kit().get_name() +
            " " +
            self._parent_command.get_name() +
            " " +
            self.get_name() +
            " <package> [options...]\n\n" +
            description
        )

    def configure_parser(self, parser):
        parser.add_argument("package", help="Package name")

    def get_name(self):
        return "remove"

    def run(self, args, terminal):
        kit = self.get_kit()
        if kit.package_is_installed(args.package):
            package_path = kit.get_full_path(kit.get_config()["packages-dir"] + "/" + args.package)
            kit.execute_shell_command("rm -rf " + package_path)
            terminal.output("The package " + args.package + " was be removed", terminal.VERBOSITY_SILENT)
        else:
            terminal.output("The package " + args.package + " is not installed", terminal.VERBOSITY_SILENT)
