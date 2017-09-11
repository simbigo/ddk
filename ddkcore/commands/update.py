import base64
import os
import sys
import urllib2

from ddkcore.command import Command


class UpdateCommand(Command):

    def configure(self):
        description = "Update ddk to the latest version."
        self.set_description(description)
        self.set_usage(
            self.get_kit().get_name() +
            " " +
            self.get_name() +
            " [options...]\n\n" +
            description
        )

    def download(self, url, auth_user=None, auth_pass=None):
        request = urllib2.Request(url)
        if auth_user is not None and auth_pass is not None and auth_user != "" and auth_pass != "":
            base64string = base64.b64encode('%s:%s' % (auth_user, auth_pass))
            request.add_header("Authorization", "Basic %s" % base64string)

        try:
            response = urllib2.urlopen(request)
        except IOError, e:
            terminal = self.get_kit().get_terminal()
            terminal.output("The username or password is wrong.", terminal.VERBOSITY_SILENT, terminal.COLOR_RED)
            sys.exit(1)

        return response.read()

    def get_name(self):
        return 'update'

    def remove_backup(self, exe_path, exe_name):
        backup_file = exe_path + "/" + exe_name + ".back"
        self.get_kit().execute_shell_command("rm " + backup_file)

    def run(self, args, terminal):
        kit = self.get_kit()
        config = kit.get_config()
        url = config["ddk-server"]["url"]
        user = config["ddk-server"]["basic-auth"]["user"]
        password = config["ddk-server"]["basic-auth"]["password"]
        if user == "":
            user = terminal.input("Type username to Basic-Auth: ")
        if password == "":
            password = terminal.input_password("Type password to Basic-Auth: ")

        exe_path = kit.get_exe_path()
        exe_name = sys.argv[0].split(os.path.sep)[-1]
        current_file = exe_path + "/" + exe_name
        backup_file = current_file + ".back"
        update_file = current_file + ".update"

        terminal.output("Current version:\n" + kit.get_version())
        terminal.output("Update...")
        data = self.download(url, user, password)

        kit.execute_shell_command("cp " + current_file + " " + backup_file)
        kit.execute_shell_command("cp " + current_file + " " + update_file)

        ddk_file = open(update_file, "w")
        ddk_file.write(data)
        ddk_file.close()

        os.rename(update_file, current_file)
        kit.execute_shell_command(current_file + " version")
