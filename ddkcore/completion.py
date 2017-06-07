import os
import subprocess

import sys


class Completion(object):

    def __init__(self, ddk):
        exe_path = ddk.get_exe_path()
        exe_name = sys.argv[0].split(os.path.sep)[-1]
        ddk_file = exe_path + "/" + exe_name
        self.__ddk = ddk
        self.__ddk_path = ddk_file

    def get_completion_package_update(self, word_number, input_list):
        return self.__ddk.get_list_of_packages()

    def get_completion_project_get(self, word_number, input_list):
        return self.__ddk.get_list_of_projects()

    def get_completion_project_init(self, word_number, input_list):
        return self.__ddk.get_list_of_projects()

    def parse(self, word_number, input_list):
        word_number = int(word_number)

        if input_list[-1][0] == "-":
            cmd = input_list[0:word_number]
            cmd[0] = "" + self.__ddk_path + ""
            cmd.append("--help")
            result = self.parse_options(cmd)
        else:
            if word_number == 1 or word_number == 2:
                cmd = input_list[0:word_number]
                cmd[0] = self.__ddk_path
                cmd.append("--help")
                result = self.parse_commands(cmd)
            else:
                command_name = input_list[1] + "_" + input_list[2]
                completion_method = getattr(self, "get_completion_" + command_name, None)
                if callable(completion_method):
                    result = completion_method(word_number, input_list)
                else:
                    result = [""]

        print " ".join(result)

    def parse_commands(self, cmd):
        help_string = subprocess.check_output(cmd)
        help_lines = help_string.split("\n")
        result = []
        skip = True
        for line in help_lines:
            if not skip:
                result.append(line[0:22].strip())
            elif line == "Available commands:" or line == "Available actions:":
                skip = False
        return result

    def parse_options(self, cmd):
        try:
            help_string = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            return [""]

        help_lines = help_string.split("\n")
        result = []
        skip = True
        for line in help_lines:
            if not skip:
                if line == "":
                    skip = True
                else:
                    result.append(line[0:22].strip())
            elif line == "Options:":
                skip = False

        cleaned_result = []
        for option_info in result:
            parts = option_info.split(",")
            for part in parts:
                part = part.strip()
                if part.startswith("--"):
                    cleaned_result.append(part.split(" ")[0])

        return cleaned_result
