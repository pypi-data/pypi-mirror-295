# PyScript.com CLI

This is a plugin for the `pyscript cli` that provides sub-commands for interacting
with pyscript.com.

# User guide

## PyScript Flow

The command line tool is an essential way of fostering a PyScript development
"flow". **This is an early draft of what such a flow might be**, and we welcome
feedback, ideas and constructive feedback as we work towards a proper release.
Since this is alpha software, anything might (and probably will) change, thanks
to your feedback. At this stage, we want to solidify the "flow" and commands
into a beta release we can share more publicly.

The Python module and remote API to which it calls will also develop as we hone
Anaconda's offering to the PyScript community and help tool authors integrate
such functionality into their code (such as code editors, CI integrations
and so on).

### Installation

To get started, you can install the `pyscript-dot-com-cli` package via pip:

```bash
$ pip install pyscript-dot-com-cli
$ pscript
$ pyscript

 Usage: pyscript [OPTIONS] COMMAND [ARGS]...

 Command Line Interface for PyScript. Run `pyscript setup` to setup the CLI interactively.

╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --version          Show project version and exit.                                                                                              │
│ --help             Show this message and exit.                                                                                                 │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ config    Display your settings.                                                                                                               │
│ copy      Copy the project. Project can be either be identified using the project ID or the combination of username and project slug.          │
│ create    Create a new pyscript project with the passed in name, creating a new directory in the current directory. Alternatively, use         │
│           `--wrap` so as to embed a python file instead.                                                                                       │
│ delete    Delete the current project if inside a project folder. Can also delete a project by its ID or slug. Can also delete all projects via │
│           `--all`.                                                                                                                             │
│ download  Download the project. Project can be either be identified using the project ID or the combination of username and project slug in    │
│           the following format: @USERNAME/SLUG, eg: @fpliger/location-api                                                                      │
│ info      Show information of the current project.                                                                                             │
│ list      List projects associated with a particular user or matching a certain criteria. The output is sorted by project slug.                │
│ login     Login to pyscript.com, use `--api_key` to login via API key. By default it will open a browser window to login via the web           │
│           interface.                                                                                                                           │
│ logout    Logout of pyscript.com.                                                                                                              │
│ ping      Ping the API to ensure settings / authentication.                                                                                    │
│ run       Creates a local server to run the app on the path and port specified.                                                                │
│ setup     Get started with the pyscript.com CLI by running a walkthrough setup.                                                                │
│ upload    Upload the current project.                                                                                                          │
│ version   Manage project versions.                                                                                                             │
│ view      View the current project in a browser.                                                                                               │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

This will also install the base `pyscript cli` package for you.

### Setting up the CLI

Once you have the CLI installed, log in to pyscript.com. To help with this, you can run
the command `pyscript setup` and go through the setup process, which will prompt
you for various details so that you can get up and running.

```bash
$ pyscript setup
...
Let's get your CLI setup with Pyscript.com, do you already have an account? [y/N]:
```


### Create a new PyScript project

```bash
$ pyscript create demo-project
App description: This is a human-readable description of the project.
Author name: Nicholas H.Tollervey
Author email: ntollervey@anaconda.com
$ cd demo-project
$ ls
index.html    main.py       pyscript.toml
```

The new project is instantiated with three files:

* `index.html` (containing all the basic scaffolding code for "Hello World!"),
* `main.py` (a simple Python script that prints "Hello World!"),
* `pyscript.toml` (containing project metadata).

Edit `index.html` or `main.py` to get going.

See your work locally via:

```bash
$ pyscript run
Serving from ~/demo-project at port 8000. To stop, press Ctrl+C.
```


### Upload a project to pyscript.com

After making some changes to your project, you can run the command:

```bash
$ pyscript upload
Contacting the mother ship...
Uploading project files...
Found 3 new files present locally, but not on pyscript.com:
        - main.py
        - pyscript.toml
        - index.html

Found 0 files locally that differ in content from what is present on pyscript.com:

Uploading new as well as modified files present locally.
OK.
To see your changes online type: pyscript view
```

### View your project on pyscript.com

We can now view the project online by running:

```bash
$ pyscript view
Opening url: https://fabiorosado.pyscriptapps.com/demo-project/
OK.
```

Note that the command `pyscript view` will take you to your default version which in this
case will be `latest`


### Release a new version of your project

Let's now create a version of your project, his is useful if you want to share your
project with others at a specific point in time.

```bash
$ pyscript version create
OK. Version v1 created.
URL: https://fabiorosado.pyscriptapps.com/demo-project/v1/
```

You can now share the url with others, you can also pass the version to the `pyscript view` command to
see this specific version

```bash
$ pyscript view v1
Opening url: https://fabiorosado.pyscriptapps.com/demo-project/v1/
OK.
```

### Other helpful commands

#### Ping the API to ensure connection

```bash
$ pyscript ping
OK. Pong.
```


#### List all your pyscript.com projects

```bash
$ pyscript list
demo-project (id: c58b3a34-6ad3-413f-b569-93bce7194e16)
OK. 1 projects found.
```

### Delete a project from pyscript.com

```bash
$ pyscript delete c58b3a34-6ad3-413f-b569-93bce7194e16
Are you sure you want to delete this project? [y/N]: y
OK.
```

### Log out of pyscript.com (Locally)

```bash
$ pyscript logout
OK. See you soon!
```
