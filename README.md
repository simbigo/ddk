# ddk

ddk  is a tool to manage of environment for projects

ddk (Docker Development Kit) is a tool that helps manage environment dependencies for projects that use docker containers.


#### Quick start

Get the latest ddk build:

```bash
wget https://github.com/simbigo/ddk/raw/master/dist/ddk
mv ddk /usr/local/bin/
chmod +x /usr/local/bin/ddk
```

Configure domain:

```
echo 127.0.0.1   hello.ddk  >> /etc/hosts
```

Run demo application:

```
$ ./ddk init
$ ./ddk project get hello
$ ./ddk compose --up
```

Now you can access the application in your browser at http://hello.ddk.

#### Configuration

To start using ddk you need is a ddk.json file. This file describes the basic configurations of the tool. If this file is not in the current directory, the script will try to find the configuration in the parent directories.

Run init command to create the file of configuration. It takes a snapshot of the default configuration and generate ddk.json based on it.

Available parameters:

| Параметр                          | Значение                    | Описание
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



#### Packages

##### Installation

```bash
$ ddk package install package-name
```


##### Create your own packages

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



#### Projects

Ddk allows you to easily configure a existing project and automatically install the necessary packages. By default, all projects will be located in the directory ```share/var/www```. The ```project list``` command shows a list of available projects.

```bash
$ ddk project list
Active projects:
   - example.dev
   - ddk.domain.dev
```

@todo


```
$ ddk project get my.project.ru
```

#### Variables

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


#### Run services

@todo

```
$ ddk compose
$ docker-compose up -d
```


#### Commands and options

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
