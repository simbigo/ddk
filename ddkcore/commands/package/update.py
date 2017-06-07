import os

from ddkcore.command import Command


class UpdateCommand(Command):

    def configure(self):
        description = "Update ddk package."
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
        parser.add_argument("packages", help="List of packages.", nargs="*", default="*")
        parser.add_argument("--no-post-install", help="Don't run post ddk-post-install commands.", action="store_true")

    def get_name(self):
        return "update"

    def run(self, args, terminal):
        kit = self.get_kit()
        config = kit.get_config()
        terminal = kit.get_terminal()

        if args.packages == "*":
            packages = []
            packages_dir = config["packages-dir"]
            terminal.output("Scanning " + kit.get_full_path(packages_dir), terminal.VERBOSITY_DEBUG)
            if os.path.isdir(packages_dir):
                packages = kit.get_list_of_packages()
                for package in packages:
                    terminal.output("  - " + package, terminal.VERBOSITY_DEBUG)
        else:
            packages = args.packages

        for package in packages:
            terminal.output("Updating of package " + package + "...")
            git_dir = kit.get_full_path(config["packages-dir"] + "/" + package)
            cmd = "cd " + git_dir + " && git pull origin master"
            kit.execute_shell_command(cmd)

            if not args.no_post_install:
                kit.execute_shell_command("cd " + kit.get_work_dir())
                kit.call_package_post_install(package)
