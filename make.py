#!/usr/bin/env python2
import subprocess

lock_file = open("dist/version.lock", "r")
last_version = lock_file.readline().strip()
version = raw_input("Type current version (last version is '" + last_version + "'): ")
lock_file.close()


source_version_string = '__ddk_version__ = "%DDK_VERSION%"'
result_version_string = '__ddk_version__ = "' + version + '"'

source_file = open('ddk.py', 'r')
source_data = source_file.read()
source_file.close()

source_data_with_version = source_data.replace(source_version_string, result_version_string)

source_file = open('ddk.py', 'w')
source_file.write(source_data_with_version)
source_file.close()

subprocess.call("pyinstaller --onefile ddk.py", shell=True)

source_file = open('ddk.py', 'w')
source_file.write(source_data)
source_file.close()

lock_file = open("dist/version.lock", "w")
lock_file.write(version)
lock_file.close()
