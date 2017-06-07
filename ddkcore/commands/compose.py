from ddkcore.command import Command
import os


class ComposeCommand(Command):

    def __merge_configs(self, first_config, second_config):
        result_config = first_config.copy()
        for key in second_config.keys():
            append_value = second_config[key]
            if key in result_config:
                if not isinstance(append_value, list):
                    append_value = [append_value]
                if not isinstance(result_config[key], list):
                    result_config[key] = [result_config[key]]
                for val in append_value:
                    result_config[key].append(val)
            else:
                result_config[key] = append_value
        return result_config

    def configure(self):
        description = "Generate docker-compose.yml"
        self.set_description(description)
        self.set_usage(
            self.get_kit().get_name() +
            " " +
            self.get_name() +
            " [<project-1> <project-2> ... <project-N>] [options...]\n\n" +
            description
        )

    def configure_parser(self, parser):
        parser.add_argument("projects", help="List of projects", nargs="*", default="*")
        parser.add_argument("--up", help="Run docker-compose up command", action="store_true")

    def get_name(self):
        return 'compose'

    def run(self, args, terminal):
        kit = self.get_kit()
        kit.ensure_projects_dir()
        kit.ensure_packages_dir()

        required_packages = {}
        if args.projects == "*":
            args.projects = kit.get_list_of_projects()

        config = kit.get_config()
        for project in args.projects:
            terminal.output("* Checking " + project, terminal.VERBOSITY_VERBOSE)
            project_config_path = config["projects-base-dir"] + "/" + project + "/" + config["projects-ddk-path"]
            if os.path.exists(project_config_path):
                project_config = kit.read_configuration_file(project_config_path)
                if "packages" in project_config:
                    for package in project_config["packages"]:
                        if isinstance(package, dict):
                            package_name = package["name"]
                            package_config = package.copy()
                            del package_config["name"]
                        else:
                            package_name = package
                            package_config = {}

                        if not (package_name in required_packages):
                            required_packages[package_name] = {}

                        for attribute in package_config.keys():
                            value = package_config[attribute]
                            variables = {
                                "package_path": kit.get_full_path(config["packages-dir"] + "/" + package_name),
                                "project_path": kit.get_full_path(config["projects-base-dir"] + "/" + project),
                                "project_dir": project,
                            }
                            if type(value) is list:
                                new_value = []
                                for item_value in value:
                                    new_value.append(kit.resolve_variables(item_value, **variables))
                                value = new_value
                            else:
                                value = kit.resolve_variables(value, **variables)
                            package_config[attribute] = value

                        required_packages[package_name] = self.__merge_configs(
                            required_packages[package_name],
                            package_config
                        )
            else:
                terminal.output("  Not found: " + kit.get_full_path(project_config_path), terminal.VERBOSITY_DEBUG)

        for package in required_packages.keys():
            if not kit.package_is_installed(package):
                terminal.output("Installing " + package + "...", terminal.VERBOSITY_VERBOSE)
                kit.install_package(package)

        terminal.output("Generating docker-compose.yml", terminal.VERBOSITY_VERBOSE)
        yml = "version: '3'\n\n"
        yml += "services:\n"
        indent = '    '
        for package in sorted(required_packages.keys()):
            yml += indent + package + ":\n"
            package_dir = config["packages-dir"] + "/" + package
            package_config_path = package_dir + "/ddk.json"
            terminal.output("Reading " + kit.get_full_path(package_config_path), terminal.VERBOSITY_DEBUG)
            package_config = kit.read_configuration_file(package_config_path)
            package_config = self.__merge_configs(package_config, required_packages[package])
            package_config["networks"] = [config["network-name"]]
            for attribute in sorted(package_config.keys()):
                if attribute.startswith("ddk-"):
                    continue

                value = package_config[attribute]
                yml += (2 * indent) + attribute + ": "
                variables = {"package_path": kit.get_full_path(package_dir)}
                if type(value) is list:
                    value = list(set(value))  # remove duplicates
                    for item in sorted(value):
                        item = kit.resolve_variables(item, **variables)
                        yml += "\n" + (3 * indent) + "- " + item
                    yml += "\n"
                else:
                    value = kit.resolve_variables(value, **variables)
                    yml += value + "\n"

        yml += "\nnetworks:\n"
        yml += indent + config["network-name"] + ": \n"
        yml += (2 * indent) + "driver: bridge"

        compose_file = "docker-compose.yml"
        f = open(compose_file, 'w')
        f.write(yml)
        f.close()
        terminal.output("File successfully generated: " + kit.get_full_path(compose_file), 0, terminal.COLOR_GREEN)

        if args.up:
            kit.execute_shell_command("docker-compose up -d")
