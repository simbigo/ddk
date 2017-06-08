# ddk

@todo


#### Quick start


@todo


```
$ ./ddk init
$ ./ddk project get my.project.ddk
$ ./ddk compose --up
```

Configure domain:

```
echo 127.0.0.1    my.project.ddk  >> /etc/hosts
```


#### Configuration

В большинстве случаев будет достатачно предустановленных значений в
конфигурации, но при необходимости ddk позволяет изменить стандартное
поведение. При запуске любой из команд, скрипт ищет в текущей директории
файл с именем ```ddk.json```, в котором и можно указать свои собственные
настройки. Если в текущей директории данный файл отсутствует, скрипт
попытается найти конфигурацию в родительских директориях. Поиск
прекращается как только файл конфигурации успешно найден или достигнут
корень файловой системы.

Для начала работы с ddk необходимо инициализировать рабочее окружение.
Сделать это можно вызвав команду ```init```, которая сделает снимок
конфигурации по умолчанию и сгенерирует на его основе ```ddk.json```.

Available parameters:

 * ```network-name``` - Network name to use docker-compose
 * ```packages-dir``` - Defaults to ```packages```. Stores all configurations of packages
 * ```share-dir``` - Defaults to ```share```. Stores data shared between containers
 * ```projects-base-dir``` - Defaults to ```share/var/www```. Stores source code of projects
 * ```projects-ddk-path``` - Defaults to ```ddk.json```
 * ```project-repo-prefix``` - The url prefix to use ```project install``` command
 * ```package-repo-prefix``` - The url prefix to use ```package install``` command
 * ```ddk-server.url``` - @todo
 * ```ddk-server.basic-auth.user``` - @todo
 * ```ddk-server.basic-auth.password``` - @todo


#### Packages

@todo


##### Installation

@todo

```
$ ddk package install package-name
```


##### Create your own packages

@todo



#### Projects

@todo

```
$ ddk project get my.project.ru
```



#### Variables

@todo

Available variables:



 * ```${NETWORK_NAME}``` - @todo
 * ```${PACKAGE_PATH}``` - @todo
 * ```${PACKAGES_PATH}``` - @todo
 * ```${PROJECT_DIR}``` - @todo
 * ```${PROJECT_PATH}``` - @todo
 * ```${PROJECTS_PATH}``` - @todo
 * ```${SHARE_PATH}``` - @todo


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

* SILENT (по умолчанию)
* VERBOSE
* DEBUG

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

 * ```--up``` - runs `docker-compose up -d` after generation

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

 * ```--no-post-install``` - disallow to run commands from init section

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
