import sys
import os


def getImports():
    before = list(sys.modules.keys())
    import test  # noqa: F401

    after = list(sys.modules.keys())

    new = [module for module in after if module not in before]
    modules = set([new_module.split(".")[0] for new_module in new])

    return modules


def findModules(imports):
    modules = {}
    paths = sys.path
    paths[0] = os.getcwd()

    for path in paths:
        for root_path, directory_names, file_names in os.walk(path):
            for i in imports:
                files = [file for file in file_names if file.startswith(f"{i}.py")]
                for file in files:
                    file_path = os.path.join(root_path, file)
                    if i in modules:
                        modules[i].append(file_path)
                    else:
                        modules[i] = [file_path]
    return modules


imports = getImports()
modules = findModules(imports)

for module in modules:
    if len(modules[module]) > 1:
        print(f"Duplicate versions of {module} found:")
        for path in set(modules[module]):
            print(f"\t{path}")
