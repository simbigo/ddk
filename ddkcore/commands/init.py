import os

from ddkcore.command import Command
import json


class InitCommand(Command):

    def configure(self):
        description = "Generate config file for Docker Development Kit."
        self.set_description(description)
        self.set_usage(
            self.get_kit().get_name() +
            " " +
            self.get_name() +
            " [options...]\n\n" +
            description
        )

    def get_name(self):
        return "init"

    def run(self, args, terminal):
        kit = self.get_kit()

        config = kit.get_config(False)
        config_path = os.getcwd() + "/" + config["config-name"]

        del config["config-name"]
        config_data = json.dumps(config, indent=4, sort_keys=True)
        f = open(config_path, 'w')
        f.write(config_data)
        f.close()

        terminal.output('Initialized ddk in ' + config_path, 0, terminal.COLOR_GREEN)
