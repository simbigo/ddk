import os

import sys

from ddkcore.command import Command
import json


class BashCompletionCommand(Command):

    __completion_script="""
_ddk()
{
    local cur
    COMPREPLY=()
    cur=${COMP_WORDS[COMP_CWORD]}
    COUNTER=0
    LIMIT=`expr $COMP_CWORD + 1`

    JOINED=""
    while [ "$COUNTER" -lt "$LIMIT" ] ; do
        WORD=${COMP_WORDS[$COUNTER]}
        JOINED="$JOINED $WORD"
        COUNTER=`expr $COUNTER + 1`
    done
    COMPREPLY=( $(compgen -W "$(%DDK_SCRIPT_PATH% get-bash-completion ${COMP_CWORD} ${JOINED})" -- ${cur}) )
    return 0
}
complete -F _ddk ddk
    """

    def configure(self):
        description = "Configure scripts to bash completion."
        self.set_description(description)
        self.set_usage(
            self.get_kit().get_name() +
            " " +
            self.get_name() +
            "\n\n" +
            description
        )

    def get_name(self):
        return "bash-completion"

    def run(self, args, terminal):
        if os.geteuid() != 0:
            msg = "Sorry, you must have admin rights. Try to use: sudo " \
                  + self.get_kit().get_name() + " " + self.get_name()
            terminal.output(msg)
            sys.exit(1)

        kit = self.get_kit()
        exe_path = kit.get_exe_path()
        exe_name = sys.argv[0].split(os.path.sep)[-1]
        ddk_file = exe_path + "/" + exe_name

        script = self.__completion_script.replace("%DDK_SCRIPT_PATH%", ddk_file)
        script_path = "/etc/bash_completion.d/"
        if os.path.exists(script_path):
            f = open(script_path + "/ddk", "w")
            f.write(script)
            f.close()
            terminal.output("OK. Refresh your bash completion.", text_format=terminal.COLOR_GREEN)
        else:
            terminal.output("The directory " + script_path + " doesn't exist.", text_format=terminal.COLOR_RED)
