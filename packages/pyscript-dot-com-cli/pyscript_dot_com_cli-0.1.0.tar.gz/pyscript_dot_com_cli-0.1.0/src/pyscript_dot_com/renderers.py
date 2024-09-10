from pathlib import Path

from rich.table import Table

from pyscript import console

VALUES_TO_HIDE = ["api_base", "api_prefix"]

projects_columns = ["project_slug", "project_name", "project_id"]
projects_table = Table(title="Projects")
projects_table.add_column("Project Slug", style="cyan")
projects_table.add_column("Project Name", style="green")
projects_table.add_column("Project ID", style="white", justify="right")

version_columns = ["version", "url", "updated_at"]
versions_table = Table(title="Versions")
versions_table.add_column("Version", style="cyan", no_wrap=True)
versions_table.add_column("URL", style="green")
versions_table.add_column("Updated at", style="white")

info_table = Table(title="Project Metadata")
info_table.add_column("Key", style="cyan", no_wrap=True)
info_table.add_column("Value", style="white", justify="right")

config_table = Table(title="PyScript.com CLI Configuration")
config_table.add_column("Config", style="cyan", no_wrap=True)
config_table.add_column("Value", style="white", justify="right")

ignore_table = Table(title="PyScript.com CLI Ignore Files List", width=35)
ignore_table.add_column("Value", style="cyan", no_wrap=True)

config_sources_table = Table(title="PyScript.com CLI Config Sources")
config_sources_table.add_column("Filepath", style="cyan", no_wrap=True)


def display_files(files, title="Files"):
    """
    Displays data present in files in a Table. Creates a new table
    every time this function is called.
    """
    files_columns = ["path", "size", "updated_at"]

    # rich doesn't have an API to clear rows of an existing Table
    # re-initializing the table does the trick for us
    files_table = Table(title=title)
    files_table.add_column("Path", style="cyan")
    files_table.add_column("Size", style="green")
    files_table.add_column("Updated at", style="white")

    for file_data in files:
        files_table.add_row(*[file_data[col] for col in files_columns])

    console.print(files_table)


def display_projects(projects):
    for project_data in projects:
        projects_table.add_row(*[project_data[col] for col in projects_columns])

    console.print(projects_table)


def display_versions(versions):
    for version in versions:
        versions_table.add_row(*[version[col] for col in version_columns])

    console.print(versions_table)


def display_manifest(manifest):
    for values in manifest.items():
        info_table.add_row(*values)

    console.print(info_table)


def display_config(config):
    for values in config.dict().items():
        if values[0] == "ignore":
            for line in values[1]:
                ignore_table.add_row(line)
        elif values[0] == "archive_ignore":
            config_table.add_row(values[0], ", ".join(values[1]))
        else:
            if values[0] not in VALUES_TO_HIDE:
                config_table.add_row(*values)

    for filepath in config.Config.env_file:
        if Path(filepath).exists():
            label = f"{filepath} ✅"
        else:
            label = f"{filepath} ❌ (not found)"
        config_sources_table.add_row(label)

    console.print(config_table)
    console.print(ignore_table)
    console.print(config_sources_table)
