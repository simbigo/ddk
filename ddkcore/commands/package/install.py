from ddkcore.command import Command


class InstallCommand(Command):

    def configure(self):
        description = "Install ddk package."
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
        return "install"

    def run(self, args, terminal):
        kit = self.get_kit()
        kit.ensure_packages_dir()
        if kit.package_is_installed(args.package):
            terminal.output("The service " + args.package + " is installed", terminal.VERBOSITY_SILENT)
            return

        kit.install_package(args.package)
