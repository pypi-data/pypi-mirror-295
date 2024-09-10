import glob
import os
import string
import subprocess
import sys
import typer

from zipfile import ZipFile
import requests
from pathlib import Path
from art import *
from typing_extensions import Annotated
from rich import print
from rich import print_json

# TODO config get-contexts could show contexts
# TODO config delete-context [context] could be a useful command
# TODO rollback command - but rollback to what?
# TODO recommend installation via pipx to isolate virtualitics-cli from project environments

# TODO this is actually printing on every single command, which is entertaining for the moment
app = typer.Typer(name="vaip", pretty_exceptions_show_locals=False,
                  help=tprint("Virtualitics AI Platform", font="cybermedium"))
debug_state = {"verbose": False}

DEFAULT_CONTEXT_PATH = "~/.virtualitics/config.conf"


def get_current_context():
    context = []
    config_path = os.path.expanduser(DEFAULT_CONTEXT_PATH)
    if os.path.exists(config_path):
        with open(os.path.expanduser(DEFAULT_CONTEXT_PATH), "r") as f:
            context_lines = f.readlines()
            try:
                if "current_context=" not in context_lines[0]:
                    print("The `current_context` was not found within the configuration file. "
                          "Perhaps run `vaip config`, or `vaip use-context`.")
                    raise typer.Exit(code=1)
                current_context = context_lines[0].split("=")[1]
            except IndexError:
                print("Your configuration file appears to be invalid. "
                      "Perhaps run `vaip config`, or `vaip use-context`.")
                raise typer.Exit(code=1)

            for i, line in enumerate(context_lines[2:]):
                if current_context.strip() in line.strip():
                    context = context_lines[i + 3:i + 6]
                    break
    else:
        print("No context file was found, please create one using `vaip config`.")

    host = context[0].split("=")[1].strip()
    token = context[1].split("=")[1].strip()
    username = context[2].split("=")[1].strip()

    return host, token, username


def write_config(file, name, host, token, username, new_file):
    with open(file, "a+") as f:
        if new_file:
            new_content = [f"current_context={name}\n\n", f"[{name}]\n", f"hostname={host}\n", f"token={token}\n",
                           f"username={username}\n\n"]
        else:
            new_content = [f"[{name}]\n", f"hostname={host}\n", f"token={token}\n", f"username={username}\n\n"]
        f.writelines(new_content)


def update_context(file: Path, context: str) -> str:
    """
    :param file: The path or path like object where the context is located
    :param context: The new context to use and write to the file
    :return: str, a message to display upon success or failure
    """
    try:
        with open(file, "r+") as f:
            lines = f.readlines()
            if any(ctx in f"[{context}]\n" for ctx in lines):
                lines[0] = f"current_context={context}\n"
                f.seek(0)
                f.writelines(lines)
                return f"Context updated to use {context}"
            else:
                return (f"Context {context} could not be used, please make sure the config file contains the "
                        f"{context} context")
    except Exception as e:
        return f"There was an error updating the context: {e}"


def app_name_callback(ctx: typer.Context, app_name: str) -> str | None:
    if ctx.resilient_parsing:
        return
    invalid_characters = set(string.punctuation.replace("_", ""))
    if any(char in invalid_characters for char in app_name):
        raise typer.BadParameter("Invalid project name. The only special character allowed is '_'.")
    else:
        return app_name


# TODO may want this
def check_config_file_exists() -> bool:
    return True


@app.callback()
def main(verbose: bool = False):
    """
    Used to enable debug logs
    """
    # TODO write some actual debug logs so this does something
    if verbose is True:
        debug_state["verbose"] = True


# TODO, confirmation prompt with all inputs displayed y/n
# TODO, disallow duplicate configs
# https://typer.tiangolo.com/tutorial/app-dir/
@app.command()
def config(name: Annotated[str, typer.Option("--name", "-N",
                                             help="User-specified friendly name for a given "
                                                  "VAIP instance, i.e. predict-dev",
                                             prompt=True)],
           host: Annotated[str, typer.Option("--host", "-H",
                                             help="Backend hostname for a given VAIP instance, "
                                                  "i.e. https://predict-api-dev.virtualitics.com",
                                             prompt=True)],
           token: Annotated[str, typer.Option("--token", "-T",
                                              help="API token used to verify the user’s access "
                                                   "to the given VAIP instance",
                                              prompt=True)],
           username: Annotated[str, typer.Option("--username", "-U",
                                                 help="Username associated with API token",
                                                 prompt=True)]

           ):
    """
    Used to create a configuration file in ~/.virtualitics/config.conf (DEFAULT_CONTEXT_PATH)
    Requires a friendly name of a VAIP instance, host of a VAIP instance, and an API token.
    """
    config_path = os.path.expanduser(DEFAULT_CONTEXT_PATH)
    config_path_no_file = os.path.expanduser("~/.virtualitics")
    config_file = Path(config_path)
    if os.path.exists(config_path):
        write_config(config_file, name, host, token, username, False)
        print(f"the configuration file of the VAIP virtualitics-cli has been updated at {config_path}")
    # directory exists, but file does not
    elif os.path.exists(config_path_no_file):
        write_config(config_file, name, host, token, username, True)
        print(f"the configuration file of the VAIP virtualitics-cli has been created at {config_path}")
    else:
        config_file.parent.mkdir(exist_ok=False, parents=True)
        write_config(config_file, name, host, token, username, True)
        print(f"the configuration file of the VAIP virtualitics-cli has been created at {config_path}")
    update_context(config_file, name)


# TODO add verification that the context already exists
@app.command()
def use_context(name: Annotated[
    str, typer.Argument(help="The name of a previously configured context referenced in the configuration file")]):
    """
    Used to set the context referenced in the config file
    """
    config_path = os.path.expanduser(DEFAULT_CONTEXT_PATH)
    config_file = Path(config_path)
    if os.path.exists(config_path):
        updated_context = update_context(config_file, name)
        print(updated_context)
    else:
        print("No configuration file found. Please run `vaip config` before using this command.")
        raise typer.Exit(code=1)


# Todo make authors list
@app.command()
def init(project_name: Annotated[
    str, typer.Option("--project-name", "-n", callback=app_name_callback,
                      help="Name for the VAIP App (No spaces or special chars besides '_')", prompt=True)],
         version: Annotated[str, typer.Option("--version", "-v",
                                              help="Version for the VAIP App (0.1.0)", prompt=True)],
         description: Annotated[
             str, typer.Option("--description", "-d", help="Description for the VAIP App",
                               prompt=True)],
         authors: Annotated[str, typer.Option("--authors", "-a", help="Authors for the VAIP App (email)",
                                              prompt=True)],
         licenses: Annotated[
             str, typer.Option("--licenses", "-l", help="Licenses for the VAIP App", prompt=True)]):
    """
    Initializes a VAIP app structure, and a pyproject.toml file that looks like this:
    [project]
    name = "vaip-apps"
    version = "0.1.1"
    description = "vaip example apps"
    authors = [{name = "Virtualitics Engineering", email = "engineering@virtualitics.com"}]
    license = {text = "MIT"}
    requires-python = ">= 3.11"

    [build-system]
    requires = ["setuptools >= 61.0"]
    build-backend = "setuptools.build_meta"

    """
    project_name = project_name.lower()
    if debug_state["verbose"]:
        print(f"Creating {project_name}/__init__.py")
    os.makedirs(f"{project_name}", exist_ok=True)
    with open(f"{project_name}/__init__.py", "w"):
        pass
    if debug_state["verbose"]:
        print(f"Creating {project_name}/blueprint_docs")
    os.makedirs(f"{project_name}/blueprint_docs", exist_ok=True)
    # TODO probably create blueprint doc example here
    if debug_state["verbose"]:
        print(f"Creating __init__.py")
    with open("__init__.py", "w"):
        pass
    if debug_state["verbose"]:
        print(f"Creating pyproject.toml")
    with open("pyproject.toml", "w"):
        pass

    # TODO, what we want is some way to identify that in vaip build, that vaip init was used
    pyproject_content = ["[project]\n", f"name = \"{project_name.replace('_', '-')}\"\n",
                         f"version = \"{version}\"\n",
                         f"description = \"{description}\"\n", f"authors = [{{name = \"{authors}\"}}]\n",
                         f"license = {{text = \"{licenses}\"}}\n",
                         "requires-python = \">= 3.11\"\n\n",
                         "[build-system]\n", "requires = [\"setuptools >= 69.0\"]\n",
                         "build-backend = \"setuptools.build_meta\"\n"]
    with open("pyproject.toml", "w") as f:
        f.writelines(pyproject_content)

    print(f"Initialization of VAIP App {project_name} structure complete.")


# TODO might want this https://pypi.org/project/setuptools-scm/
@app.command()
def build(confirm_build: Annotated[bool, typer.Option("--yes", "-y",
                                                      help="Build a wheel using pyproject.toml in current directory?",
                                                      prompt=True)]):
    """
    Builds a VAIP App Python wheel file
    """
    # TODO allow building outside current directory?
    # TODO this might be different for Windows
    if not confirm_build:
        print("Did not confirm build.")
        raise typer.Exit(code=1)
    try:
        subprocess.check_call([sys.executable, '-m', 'build'])  # this might need to be adjusted for Windows
        print("Successfully built VAIP App, check your /dist directory.")
    except subprocess.CalledProcessError as e:
        print(f"There was an error during build: {e}")
        print("Try running `python -m build` if you are having issues.")


# TODO, what we want is some way to identify that in vaip build, that vaip init was used
# TODO we may want args here to specify uploading outside of the current directory
# TODO somehow make sure any requirements added don't conflict with backend or worker container
@app.command()
# https://typer.tiangolo.com/tutorial/parameter-types/path/
def deploy(file: Annotated[str, typer.Option("--file", "-f",
             help="Absolute path to the wheel file "
                  "if not in current project /dist")] = ""):
    """
    Deploys the VAIP App to a VAIP Instance
    """
    host, token, username = get_current_context()

    # else assume default dir ./dist/*.whl'
    if not file:
        try:
            file = glob.glob("./dist/*.whl")[0]
        except IndexError:
            print(
                f"Unable to locate a suitable wheel file. Perhaps try running vaip build, "
                f"or providing an absolute path with --file")
    if file.split(".")[-1] != "whl":
        print(f"File {file} does not appear to be a wheel file.")
        raise typer.Exit(code=1)
    files = {'file': open(file, 'rb')}
    if debug_state["verbose"]:
        print(f"Attempting to send files: {files}\n")
        names = ZipFile(file).namelist()
        print(f'Unzipped file contents: {names}\n')
    print(f"Using:\n username {username} \n token: ...{token[-4:]} \n host: {host} \n ")


    try:
        r = requests.post(f"{host}/cli/deploy/",
                          data={"username": username},
                          headers={"Authorization": f"Bearer {token}"},
                          files=files)
        if r.status_code == 404:
            print("Error: It looks like your VAIP instance is not configured for CLI App uploads.")
            raise typer.Exit(code=1)
        else:
            print_json(r.text)
            raise typer.Exit()
    except requests.exceptions.ConnectionError as e:
        print(f"Error: Unable to connect to {host}. Please check your connections and try again.")
        raise typer.Exit(code=1)


@app.command()
def destroy(
        project_name: Annotated[
            str, typer.Option("--project-name", "-n",
                              help="Project name to delete (ie, name in pyproject.toml)", prompt=True)],
        confirm_delete: Annotated[bool, typer.Option("--yes", "-y", prompt=True)]):
    """
    Deletes a VAIP module, and all the apps of that module.
    """
    host, token, username = get_current_context()
    if not confirm_delete:
        print("Did not confirm delete.")
        raise typer.Exit(code=1)
    try:
        r = requests.post(f"{host}/cli/delete/",
                          data={"username": username, "project_name": project_name},
                          headers={"Authorization": f"Bearer {token}"})
        if r.status_code == 404:
            print("Error: It looks like your VAIP instance is not configured for CLI App uploads.")
            raise typer.Exit(code=1)
        else:
            print(f"Instance response: {r.text}")
            raise typer.Exit()
    except requests.exceptions.ConnectionError:
        print(f"Error: Unable to connect to {host}. Please check your connections and try again.")
        raise typer.Exit(code=1)


@app.command()
def publish():
    """
    Publishes a VAIP App to other users in your group
    """
    host, token, username = get_current_context()

    r = requests.post(f"{host}/cli/publish/",
                      data={"username": username},
                      headers={"Authorization": f"Bearer {token}"})

    print(r.text)
    print("Makes the current VAIP App available to other users in your group")
