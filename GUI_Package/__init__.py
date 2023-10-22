import importlib
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


def execute_script(script_name, arg, output):
    module = get_script_module(script_name)
    return module.execute(*arg, output=output)
