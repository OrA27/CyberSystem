import importlib
import os
import pkgutil


def list_package_modules(package_name):
    """
    List all the modules of a given package, ignoring any submodules.
    """
    package = __import__(package_name)
    modules = []
    for importer, modname, ispkg in pkgutil.walk_packages(package.__path__):
        if not ispkg:
            modules.append(modname)
    return modules


def get_script_module(script_name):
    full_name = f"Cyber_Scripts.{script_name}"
    module = importlib.import_module(full_name)
    return module


def execute_script(script_name, arg):
    module = get_script_module(script_name)
    return module.execute(*arg)


def file_path(file_name: str):
    # replace spaces
    file_name = file_name.replace(" ", "_")

    # Define the path to the current Python file
    current_file_path = os.path.abspath(__file__)

    # Get the directory containing the current Python file
    current_directory = os.path.dirname(current_file_path)

    # Get the parent directory of the current directory
    parent_directory = os.path.dirname(current_directory)

    # Define the path to the new folder and the new file
    new_folder_path = os.path.join(parent_directory, "Saved")
    new_file_path = os.path.join(new_folder_path, (file_name + ".pkl"))

    # Create the new folder
    os.makedirs(new_folder_path, exist_ok=True)

    return new_file_path
