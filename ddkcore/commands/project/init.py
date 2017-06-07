from ddkcore.command import Command


class InitCommand(Command):

    def configure(self):
        description = "Run init commands from the configuration file of the project."
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

    def get_name(self):
        return "init"

    def run(self, args, terminal):
        kit = self.get_kit()
        kit.ensure_projects_dir()

        if not kit.project_exists(args.pid):
            terminal.output("Project is not installed", 0, terminal.COLOR_YELLOW)
            return

        kit.call_project_init(args.pid)
