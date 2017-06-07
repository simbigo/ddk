import argparse
import json
import os
import subprocess
import sys
from ddkcore.parser import DdkParser


class Kit(object):

    __app_description = 'Docker Development Kit'
    __app_name = 'ddk'
    __commands = {}
    __help_message = "Show this help message and exit."
    __parser = None
    __subparsers = None
    __working_directory = None

    def __init__(self, conf, app_version, terminal, exe_path):
        self.__app_version = app_version
        self.__config = None
        self.__default_config = conf
        self.__exe_path = exe_path
        self.__terminal = terminal

    def __configure_commands(self):
        for cmd_name in self.__commands.keys():
            command = self.get_command(cmd_name)
            command.configure()
            parser_config = dict(help=command.description, add_help=False, conflict_handler="resolve")
            parser = self.__subparsers.add_parser(cmd_name, **parser_config)
            self.add_default_arguments(parser)
            if command.has_sub_commands():
                command.configure_sub_commands(parser)
            else:
                command.configure_parser(parser)
                parser.set_defaults(cmd_callback=command)

            if len(command.usage) > 0:
                parser.usage = self.__commands[cmd_name].usage

    def __detect_working_dir(self):
        terminal = self.get_terminal()
        terminal.output("Detection of working directory...", terminal.VERBOSITY_DEBUG)
        current_dir = os.getcwd()
        file_name = self.__default_config["config-name"]
        result_dir = None
        while result_dir is None and current_dir != "/":
            config_file = os.path.abspath(current_dir + "/" + file_name)
            terminal.output("  - " + config_file, terminal.VERBOSITY_DEBUG)
            if os.path.isfile(config_file):
                result_dir = current_dir
            else:
                current_dir = os.path.abspath(current_dir + "/..")

        config_file = os.path.abspath(current_dir + "/" + file_name)
        if os.path.isfile(config_file):
            result_dir = current_dir

        if result_dir is None:
            terminal = self.get_terminal()
            terminal.output("Can't find ddk.json file.")
            terminal.output("Run next command if you don't have ddk environment:\n")
            terminal.output("    " + self.get_name() + " init", terminal.VERBOSITY_SILENT, terminal.COLOR_YELLOW)
            sys.exit(1)

        result_dir = os.path.abspath(result_dir)
        terminal.output("Working directory is " + result_dir, terminal.VERBOSITY_DEBUG)
        self.set_work_dir(result_dir)

    def add_command(self, cmd):
        cmd.set_kit(self)
        self.__commands[cmd.get_name()] = cmd

    def add_default_arguments(self, parser):
        quiet_help = "Operate quietly. This option disables all output."
        verbose_help = "Increases verbosity level. Does not affect if --quiet option is set."
        parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help=self.__help_message)
        parser.add_argument('-q', '--quiet', action="store_true", help=quiet_help)
        parser.add_argument('-v', '--verbose', action="count", default=0, help=verbose_help)
        parser.add_argument('-d', '--dir', help="Set up working directory.", metavar="PATH")

    def call_package_post_install(self, package):
        config = self.get_config()
        package_dir = config["packages-dir"] + "/" + package
        package_config_path = package_dir + "/ddk.json"
        package_config = self.read_configuration_file(package_config_path)
        if "ddk-post-install" in package_config:
            self.get_terminal().output("Calling post install commands...")
            for command in package_config["ddk-post-install"]:
                variables = {"package_path": self.get_full_path(package_dir)}
                command = self.resolve_variables(command, **variables)
                self.execute_shell_command(command)

    def call_project_init(self, project):
        terminal = self.get_terminal()
        if not self.project_exists(project):
            terminal.output("Project " + project + " is not installed", text_format=terminal.COLOR_RED)
            sys.exit(1)

        config = self.get_config()
        project_dir = config["projects-base-dir"] + "/" + project
        project_config_path = project_dir + "/" + config["projects-ddk-path"]
        if os.path.exists(project_config_path):
            project_config = self.read_configuration_file(project_config_path)
            if "on-init" in project_config:
                variables = {
                    "project_dir": project,
                    "project_path": self.get_full_path(project_dir),
                }
                for command in project_config["on-init"]:
                    command = self.resolve_variables(command, **variables)
                    terminal.output("    > " + command, 0, terminal.COLOR_PURPLE)
                    self.execute_shell_command(command)

    def ensure_packages_dir(self):
        """Make directory for packages if it doesn't exists"""
        dir_name = self.get_full_path(self.get_config()["packages-dir"])
        if not os.path.exists(dir_name):
            terminal = self.get_terminal()
            terminal.output("Ensure packages directory: " + dir_name, terminal.VERBOSITY_DEBUG)
            os.mkdir(dir_name)

    def ensure_projects_dir(self):
        """Make directory for projects if it doesn't exists"""
        config = self.get_config()
        projects_dir = self.get_full_path(config["projects-base-dir"])
        if not os.path.isdir(projects_dir):
            terminal = self.get_terminal()
            terminal.output("Make directory for projects: " + projects_dir, terminal.VERBOSITY_DEBUG)
            os.makedirs(projects_dir)

    def execute_shell_command(self, command):
        terminal = self.get_terminal()
        terminal.output("    > " + command, terminal.VERBOSITY_VERBOSE, terminal.COLOR_PURPLE)
        subprocess.call(command, shell=True)

    def get_command(self, name):
        return self.__commands[name]

    def get_config(self, with_user=True):
        if not with_user:
            return self.__default_config

        if self.__config is None:
            user_config_path = self.get_work_dir() + "/" + self.__default_config["config-name"]
            if os.path.exists(user_config_path):
                user_config = self.read_configuration_file(user_config_path)
            else:
                user_config = {}

            kit_configuration = self.__default_config.copy()
            kit_configuration.update(user_config)
            self.__config = kit_configuration

        return self.__config

    def get_exe_path(self):
        return self.__exe_path

    def get_full_path(self, path):
        if path.startswith("/"):
            return path

        return self.get_work_dir() + "/" + path

    def get_list_of_packages(self):
        terminal = self.get_terminal()
        packages = []
        config = self.get_config()
        packages_dir = config["packages-dir"]
        full_packages_dir = self.get_full_path(packages_dir)
        terminal.output("Scanning " + full_packages_dir, terminal.VERBOSITY_DEBUG)
        if os.path.isdir(packages_dir):
            terminal.output("Scan the packages directory: " + full_packages_dir, terminal.VERBOSITY_DEBUG)
            for package in os.listdir(full_packages_dir):
                if os.path.isdir(full_packages_dir + "/" + package):
                    packages.append(package)

        return packages

    def get_list_of_projects(self):
        """Scan the project directory to get list of available projects"""
        config = self.get_config()
        projects = []
        projects_dir = self.get_full_path(config["projects-base-dir"])
        if os.path.isdir(projects_dir):
            terminal = self.get_terminal()
            terminal.output("Scan the projects directory: " + projects_dir, terminal.VERBOSITY_DEBUG)
            for project in os.listdir(projects_dir):
                if os.path.isdir(projects_dir + "/" + project):
                    terminal.output("  - " + project, terminal.VERBOSITY_DEBUG)
                    projects.append(project)

        return projects

    def get_name(self):
        return self.__app_name

    def get_terminal(self):
        return self.__terminal

    def get_version(self):
        return self.__app_version

    def get_work_dir(self):
        if self.__working_directory is None:
            self.__detect_working_dir()
        return self.__working_directory

    def install_package(self, package):
        config = self.get_config()
        package_dir = self.get_full_path(config["packages-dir"] + "/" + package)
        clone_cmd = "git clone " + config["package-repo-prefix"][0] + package + ".git " + package_dir
        try:
            self.execute_shell_command(clone_cmd)
            self.call_package_post_install(package)
            return True
        except subprocess.CalledProcessError:
            self.get_terminal().output("Can't install the package: " + package, self.get_terminal().COLOR_RED)
            return False

    def package_is_installed(self, package):
        """Check the package is installed"""
        dir_name = self.get_full_path(self.get_config()["packages-dir"] + "/" + package)
        self.get_terminal().output("Check the " + package + " exists: " + dir_name, self.get_terminal().VERBOSITY_DEBUG)
        return os.path.exists(dir_name)

    def process(self, args):
        ddk_params = dict(
            prog=self.__app_name,
            description=self.__app_description,
            add_help=False,
            conflict_handler="resolve",
            usage="%(prog)s <command> ... [options...]"
        )
        self.__parser = DdkParser(**ddk_params)
        self.add_default_arguments(self.__parser)

        self.__subparsers = self.__parser.add_subparsers(dest="command", metavar="", title="Available commands")
        self.__configure_commands()

        args = self.__parser.parse_args(args)

        terminal = self.get_terminal()
        verbosity = args.verbose
        if args.quiet:
            verbosity = terminal.VERBOSITY_QUIET
        terminal.set_verbosity(verbosity)

        command = args.cmd_callback
        del args.cmd_callback
        del args.command

        if args.dir:
            self.set_work_dir(args.dir)

        command.run(args, terminal)

    def project_exists(self, pid):
        """Check project ID is valid item of projects list"""
        return pid in self.get_list_of_projects()

    def read_configuration_file(self, file_path):
        terminal = self.get_terminal()
        terminal.output("Reading configuration file: " + self.get_full_path(file_path), terminal.VERBOSITY_DEBUG)
        json_file = open(file_path)
        config = json.load(json_file)
        json_file.close()
        return config

    def resolve_variables(self, text, **kwargs):
        """Replace variables to passed values"""
        config = self.get_config()
        variables = {
            "network_name": config["network-name"],
            "packages_path": self.get_full_path(config["packages-dir"]),
            "projects_path": self.get_full_path(config["projects-base-dir"]),
            "share_path": self.get_full_path(config["share-dir"]),
        }
        variables.update(kwargs)

        text = str(text)
        terminal = self.get_terminal()
        terminal.output("Resolving variables for " + text, terminal.VERBOSITY_DEBUG)
        for var_name, var_value in variables.iteritems():
            text = str.replace(text, "${" + str.upper(var_name) + "}", str(var_value))
        terminal.output(" > " + text, terminal.VERBOSITY_DEBUG)
        return text

    def set_work_dir(self, work_dir):
        self.__working_directory = work_dir
        os.chdir(work_dir)
