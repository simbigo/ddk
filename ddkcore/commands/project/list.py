from ddkcore.command import Command


class ListCommand(Command):

    def configure(self):
        description = "Show all installed projects."
        self.set_description(description)
        self.set_usage(
            self.get_kit().get_name() +
            " " +
            self._parent_command.get_name() +
            " " +
            self.get_name() +
            " [options...]\n\n" +
            description
        )

    def get_name(self):
        return "list"

    def run(self, args, terminal):
        projects_list = self.get_kit().get_list_of_projects()
        terminal.output("Active projects:")
        for project in projects_list:
            terminal.output("  - " + project)
