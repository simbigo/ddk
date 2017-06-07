import os

from ddkcore.command import Command


class GetCommand(Command):

    def configure(self):
        description = "Download and configure remote project."
        self.set_description(description)
        self.set_title("Arguments")
        self.set_usage(
            self.get_kit().get_name() +
            " " +
            self._parent_command.get_name() +
            " " +
            self.get_name() +
            " " +
            "<project-id> [options...]\n\n" +
            description
        )

    def configure_parser(self, parser):
        parser.add_argument("pid", metavar="project-id", help="Project ID.")
        parser.add_argument("-t", "--target", help="Target directory. Default directory equal ID.")
        parser.add_argument("--no-init", help="Don't run init commands.", action="store_true")

    def get_name(self):
        return "get"

    def run(self, args, terminal):
        kit = self.get_kit()
        kit.ensure_projects_dir()

        if kit.project_exists(args.pid):
            terminal.output("Project is installed", 0, terminal.COLOR_YELLOW)
            return

        config = kit.get_config()
        project_dir = args.pid
        if "target" in args and args.target is not None:
            project_dir = args.target

        command = "cd " + kit.get_full_path(config["projects-base-dir"]) + \
                  " && git clone " + config["project-repo-prefix"][0] + args.pid + ".git " + project_dir
        kit.execute_shell_command(command)

        project_path = config["projects-base-dir"] + "/" + project_dir
        project_config_path = project_path + "/" + config["projects-ddk-path"]
        if os.path.exists(project_config_path):
            project_config = kit.read_configuration_file(project_config_path)
            if "packages" in project_config:
                for package in project_config["packages"]:
                    if isinstance(package, dict):
                        package_name = package["name"]
                    else:
                        package_name = package
                    if not kit.package_is_installed(package_name):
                        terminal.output("Installing " + package_name + "...", 0, terminal.COLOR_YELLOW)
                        kit.install_package(package_name)

            if not args.no_init:
                kit.call_project_init(project_dir)
