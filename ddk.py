#!/usr/bin/env python2

import os
import sys

from ddkcore.commands.completion import BashCompletionCommand
from ddkcore.commands.compose import ComposeCommand
from ddkcore.commands.init import InitCommand
from ddkcore.commands.package.package import PackageCommand
from ddkcore.commands.project.project import ProjectCommand
from ddkcore.commands.update import UpdateCommand
from ddkcore.commands.version import VersionCommand
from ddkcore.completion import Completion
from ddkcore.console import Console
from ddkcore.kit import Kit

if getattr(sys, 'frozen', False):
    ddk_path = os.path.abspath(os.path.dirname(sys.executable))
else:
    ddk_path = os.path.abspath(os.path.dirname(__file__))

default_config = {
    "config-name": "ddk.json",
    "network-name": "ddknet",
    "packages-dir": "packages",
    "share-dir": "share",
    "projects-base-dir": "share/var/www",
    "projects-ddk-path": "ddk.json",
    "project-repo-prefix": ["https://github.com/simbigo/ddk-"],
    "package-repo-prefix": ["https://github.com/simbigo/ddk-pkg-"],
    "ddk-server": {
        "url": "https://github.com/simbigo/ddk/raw/master/dist/ddk",
        "basic-auth": {
            "user": "",
            "password": ""
        }
    },
}

if len(sys.argv) < 2:
    sys.argv.append('--help')

__ddk_version__ = "%DDK_VERSION%"

ddk = Kit(default_config, __ddk_version__, Console(), ddk_path)

if sys.argv[1] == "get-bash-completion":
    completion = Completion(ddk)
    completion.parse(sys.argv[2], sys.argv[3:])
    sys.exit(0)

ddk.add_command(BashCompletionCommand())
ddk.add_command(ComposeCommand())
ddk.add_command(InitCommand())
ddk.add_command(PackageCommand())
ddk.add_command(ProjectCommand())
ddk.add_command(UpdateCommand())
ddk.add_command(VersionCommand())
ddk.process(sys.argv[1:])
