<div align="center">

<img src="https://raw.githubusercontent.com/ivnvxd/ivnvxd/master/img/h_task_manager.png" alt="logo" width="270" height="auto" />    
<h1>Task Manager</h1>

[![Actions Status](https://github.com/sergey-royt/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/sergey-royt/python-project-52/actions)
[![linter and tests](https://github.com/sergey-royt/python-project-52/actions/workflows/linter-check.yml/badge.svg)](https://github.com/sergey-royt/python-project-52/actions/workflows/linter-check.yml)
<a href="https://codeclimate.com/github/sergey-royt/python-project-52/test_coverage"><img src="https://api.codeclimate.com/v1/badges/1a2a6cfe923166d7cd63/test_coverage" /></a>

<p>

<a href="#about">About</a> •
<a href="#installation">Installation</a> •
<a href="#usage">Usage</a>
</p>

</div>

<h2>About</h2>

A task management web application built with Python and [Django](https://www.djangoproject.com/) framework. It allows you to set tasks, assign performers and change their statuses. Registration and authentication are required to work with the system.

To provide users with a convenient, adaptive, modern interface, the project uses the [Bootstrap](https://getbootstrap.com/) framework.

The frontend is rendered on the backend. This means that the page is built by the DjangoTemplates backend, which returns prepared HTML. And this HTML is rendered by the server.

[PostgreSQL](https://www.postgresql.org/) is used as the object-relational database system.

### Features

* [x] Set tasks;
* [x] Assign performers;
* [x] Change task statuses;
* [x] Set multiple tasks labels;
* [x] Filter the tasks displayed;
* [x] User authentication and registration;

### Built With

* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [Bootstrap 5](https://getbootstrap.com/)
* [PostgreSQL](https://www.postgresql.org/)
* [Poetry](https://python-poetry.org/)
* [Gunicorn](https://gunicorn.org/)
* [Whitenoise](http://whitenoise.evans.io/en/latest/)
* [Rollbar](https://rollbar.com/)
* [Flake8](https://flake8.pycqa.org/en/latest/)

### Details

For **_user_** authentication, the standard Django tools are used. In this project, users will be authorized for all actions, that is, everything is available to everyone.

Each task in the task manager usually has a **_status_**. With its help you can understand what is happening to the task, whether it is done or not. Tasks can be, for example, in the following statuses: _new, in progress, in testing, completed_.

**_Tasks_** are the main entity in any task manager. A task consists of a name and a description. Each task can have a person to whom it is assigned. It is assumed that this person performs the task. Also, each task has mandatory fields - author (set automatically when creating the task) and status.

**_Labels_** are a flexible alternative to categories. They allow you to group the tasks by different characteristics, such as bugs, features, and so on. Labels are related to the task of relating many to many.

When the tasks become numerous, it becomes difficult to navigate through them. For this purpose, a **_filtering mechanism_** has been implemented, which has the ability to filter tasks by status, performer, label presence, and has the ability to display tasks whose author is the current user.

---

## Installation

Before installing the package make sure you have Python version 3.10 or higher installed:

```bash
>> python --version
Python 3.10+
```

#### Poetry

The project uses the Poetry dependency manager. To install Poetry use its [official instruction](https://python-poetry.org/docs/#installation).

#### PostgreSQL / SQLite

There are ways for using a database management system for this project: **PostgreSQL** and **SQLite**.

PostgreSQL is used as the main database management system. You have to install it first. It can be downloaded from [official website](https://www.postgresql.org/download/) or installed using Homebrew:
```shell
>> brew install postgresql
```

_Alternatively you can skip this step and use **SQLite** database locally._

### Application

To use the application, you need to clone the repository to your computer. This is done using the `git clone` command. Clone the project:

```bash
>> git clone https://github.com/sergey-royt/python-project-52.git && cd python-project-52
```

After that install all necessary dependencies:

```bash
>> make install
```

Create `.env` file in the root folder and add following variables:
```dotenv
DATABASE_URL=postgresql://{provider}://{user}:{password}@{host}:{port}/{db}
SECRET_KEY={your secret key} # Django will refuse to start if SECRET_KEY is not set
LANGUAGE=en-us # By default the app will use ru-ru locale
```
If you choose to use **SQLite**:
```dotenv
DATABASE_URL=sqlite:///{PATH}
```

_Please check ```env_example``` files in app root directory and users app directory for more information 
about environment variables._

To create the necessary tables in the database, start the migration process:
```bash
>> make migrate
```

---

## Usage

Start the Gunicorn Web-server by running:

```shell
>> make start
```

By default, the server will be available at http://0.0.0.0:8000.

It is also possible to start it local in development mode using:

```shell
>> make dev
```

The dev server will be at http://127.0.0.1:8000.

### Makefile Commands

<dl>
    <dt><code>make install</code></dt>
    <dd>Install all dependencies of the package.</dd>
    <dt><code>make migrate</code></dt>
    <dd>Generate and apply database migrations.</dd>
    <dt><code>make dev</code></dt>
    <dd>Run Django development server at http://127.0.0.1:8000/</dd>
    <dt><code>make start</code></dt>
    <dd>Start the Gunicorn web server at http://0.0.0.0:8000 if no port is specified in the environment variables.</dd>
    <dt><code>make lint</code></dt>
    <dd>Check code with flake8 linter.</dd>
    <dt><code>make test</code></dt>
    <dd>Run tests.</dd>
    <dt><code>make shell</code></dt>
    <dd>Start Django shell (iPython REPL).</dd>
</dl>

This is the fourth and **final** training project of the ["Python Developer"](https://ru.hexlet.io/programs/python) course on [Hexlet.io](https://hexlet.io)

> GitHub [@sergey-royt](https://github.com/sergey-royt) &nbsp;&middot;&nbsp;
