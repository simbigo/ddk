# ddk

ddk (Docker Development Kit) is a tool that helps manage environment dependencies for projects that use docker containers.


### Quick start

Get the latest ddk build:

```bash
$ wget https://github.com/simbigo/ddk/raw/master/dist/ddk
$ mv ddk /usr/local/bin/
$ chmod +x /usr/local/bin/ddk
```

Configure domain:

```
$ echo 127.0.0.1   hello.ddk  >> /etc/hosts
```

Run demo application:

```
$ ddk init
$ ddk project get hello
$ ddk compose --up
```

Now you can access the application in your browser at http://hello.ddk.

### Configuration

To start using ddk you need is a ddk.json file. This file describes the basic configurations of the tool. If this file is not in the current directory, the script will try to find the configuration in the parent directories.

Run init command to create the file of configuration. It takes a snapshot of the default configuration and generate ddk.json based on it.

Available parameters:

| Parameter                         | Value                       | Description
| --------------------------------- | --------------------------- | -------------
| ddk-server.url                    |                             | The server url to get for updates
| ddk-server.basic-auth.password    |                             | Username for Basic-Auth
| ddk-server.basic-auth.user        |                             | Password for Basic-Auth
| network-name                      | ddknet                      | Network name to use docker-compose
| packages-dir                      | packages                    | Stores all configurations of packages
| projects-base-dir                 | share/var/www               | Stores source code of projects
| projects-ddk-path                 | ddk.json                    | Path to the configuration file
| share-dir                         | share                       | Stores data shared between containers
| project-repo-prefix               |                             | The url prefix to use ```project install``` command
| package-repo-prefix               |                             | The url prefix to use ```package install``` command



### Packages

#### Installation

```bash
$ ddk package install package-name
```


#### Create your own packages

Each package contains a configuration file that will be used on building of a service. In fact, this is part of the configuration of docker-compose.yml, but represents in JSON format.

```json
{
    "container_name": "my-container.dev",
    "volumes": [
        "/etc/localtime:/etc/localtime:ro",
        "${PACKAGE}/storage/etc/some/path/some.conf:/etc/some/path/some.conf:ro",
        "${SHARE}/var/www:/var/www"
    ],
    "ddk-post-install": [
        "echo 'Done'"
    ]
}
```

**Special keys:**

***ddk-post-install***

This key contains a list of commands to run after installation of the package.

**Variables**

The configuration supports using of variables. For more information see "Variable" section.



### Projects

Ddk allows you to easily configure a existing project and automatically install the necessary packages. By default, all projects will be located in the directory ```share/var/www```. The ```project list``` command shows a list of available projects.

```bash
$ ddk project list
Active projects:
   - example.dev
   - ddk.domain.dev
```

#### Run a project

To run an existing project you should use a ```get``` command.

```bash
$ ddk project get project-id
```
This command clones the project to the directory share/var/www and then the configuration file is searched for (default search in the project root) and after that all necessary commands from the section on-init are run.

#### Configure a project

To configure the project, you need to create a ddk.json file in the root directory. It contains some information for the installation.

Apart from the initialization commands, the ddk.json file contains a list of packages needed for correct work of the project. If any of the packages is missing, it will be installed automatically. Below is an example of a project configuration.

```json
{
    "packages": [
        "mysql5.5",
        "memcached",
        "apache-php5.5"
    ],
    "on-init": [
        "${PROJECT_PATH}/init.sh ${PACKAGES_PATH} ${PROJECT_DIR}"
    ]
}
```

If it is necessary to extend a configuration of any package, you can do it indicating it as an object. This object should have a name attribute containing the package name. All the rest attributes will be identified as configurations.

```json
{
    "packages": [
        {
            "name": "nginx",
            "depends_on": [
                "php-fpm7.1"
            ],
            "environment": [
                "SOME_VAR=Hello"
            ]
        }
    ]
}
```

**Variables**

The configuration supports using of variables. For more information see "Variable" section.


### Variables

In processing of the configurations, ddk checks and resolves some variables.

Available variables:

| Variable           | Availability                       | Description
| ------------------ | ---------------------------------- | -------------------
| ${NETWORK_NAME}    | everywhere                         | network name
| ${PACKAGE_PATH}    | install and update a package       | the path to the package directory
| ${PACKAGES_PATH}   | everywhere                         | the packages directory
| ${PROJECT_DIR}     | install and update a package       | the project directory
| ${PROJECT_PATH}    | install and update a package       | the full path to the project directory
| ${PROJECTS_PATH}   | everywhere                         | the path to the projects directory
| ${SHARE_PATH}      | everywhere                         | the path to the share directory


### Run services

The last thing to do is to run all necessary services using the usual docker-compose. The command compose is used to generate run options. When running it, ddk scans all active packages, collects data on packages and their parameters, merges all received information with configurations of the packages themselves and based on this data it generates a final docker-compose.yml. This file is used during the running.

```bash
$ ddk compose
$ docker-compose up -d
```

If you specify a corresponding option during the configuring, you can get by with only one command.

```bash
$ ddk compose --up
```

### Commands and options

---

**Global options**

***-d, --dir***

Setup working directory.

```
$ pwd
/home/username
$ ddk init
Initialized ddk in /home/username/ddk.json
$ ddk init --dir=/var/projects/ddk
Initialized ddk in /var/projects/ddk/ddk.json
```

***-h, --help***

Show help message.

***-q, --quiet***

Operate quietly. This option disables all output.

***-v, --verbose***

Increases verbosity level. Does not affect if --quiet option is set.
Available values:

| Name    | Options |
| ------- | ------- |
| SILENT  | default |
| VERBOSE | -v      |
| DEBUG   | -vv     |

Run command in debug mode:

```
$ ddk package install balancer -vv
```

---

**Commands**

***ddk bash-completion***

Configure scripts to bash completion

> You must have sudo privileges to run the command

***ddk compose***

Generate docker-compose.yml.

```
$ ddk compose [<project-1> <project-2> ... <project-N>] [options...]
```

| Option | Description                                  |
| ------ | -------------------------------------------- |
| --up   | runs `docker-compose up -d` after generation |

***ddk init***

Init environment to use ddk tools.

***ddk package install***

Installation of the package.

```
$ ddk package install <package> [options...]
```

***ddk package remove***

Remove the ddk-package.

```
$ ddk package remove <package> [options...]
```

***ddk package update***

Update the packages to the latest versions.

```
$ ddk package update [<package-1> <package-2> ... <package-N>] [options...]
```
| Option            | Description                                |
| ----------------- | ------------------------------------------ |
| --no-post-install | disallow to run commands from init section |

***ddk project get***

Download and configuration of the project.

```
$ ddk project get <project> [options...]
```

***ddk project init***

Run commands from on-init section.

```
$ ddk project init <project> [options...]
```

***ddk project list***

List all installed projects.

```
$ ddk project list [options...]
```

***ddk update***

Update ddk to the latest version.

```
$ ddk update [options...]
```

***ddk version***

Show the ddk version information.

```
$ ddk version
```
