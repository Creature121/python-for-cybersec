import sys
import os
import difflib


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
    paths = modules[module]
    if len(paths) > 1:
        paths = list(set(paths))
        pairs_of_paths = list(zip(paths, paths[1:]))
        contents_of_pairs_of_paths = [
            (
                open(path_a, "r", encoding="utf-8", errors="ignore").readlines(),
                open(path_b, "r", encoding="utf-8", errors="ignore").readlines(),
            )
            for (path_a, path_b) in pairs_of_paths
        ]
        paths_and_contents = zip(pairs_of_paths, contents_of_pairs_of_paths)

        diffs_of_pairs = [
            difflib.unified_diff(lines_1, lines_2, fromfile=file_1, tofile=file_2)
            for ((file_1, file_2), (lines_1, lines_2)) in paths_and_contents
        ]

        to_print = [
            elem
            for (path, diff_lines) in zip(paths, diffs_of_pairs)
            for elem in ([path] + [f"\t\t{line}" for line in list(diff_lines)])
        ]

        print(f"Duplicate versions of {module} found:")
        for i in to_print:
            print(i)
