import os
import string

from parser.Library import Library
from parser.LibraryGroup import LibraryGroup
from parser.Variable import Variable


class Parser:
    lib_groups = set()
    variables = {}

    def __init__(self):
        self.lib_groups = set()
        self.variables = {}

    def get_libraries(self, directory) -> set[LibraryGroup]:
        gradle_files = self.__find_gradle_files(directory)

        for file in gradle_files:
            with open(file, 'r') as kts_file:
                lines = kts_file.readlines()
                self.__parse(lines)

        return self.lib_groups

    def __find_gradle_files(self, directory):
        gradle_files = []

        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".kts"):
                    gradle_files.append(os.path.join(root, file))

        return gradle_files

    def __parse(self, lines: list[str]):
        start_parse = False

        for line in lines:
            if "dependencies" in line:
                start_parse = True

            if start_parse and "}" in line:
                start_parse = False

            if start_parse:
                lib = self.__try_get_library_from_line(line)
                if lib is not None:
                    self.__add_lib(lib)
                else:
                    var = self.__check_for_variable(line)
                    if var is not None:
                        self.variables[var.name] = var.value

    def __try_get_library_from_line(self, line: str) -> Library | None:
        if len(line) > 0:
            tokens = (line.replace('(', ':')
                      .replace(')', '')
                      .replace('"', '')
                      .replace(' ', '')
                      .replace('\n', '')
                      .split(':'))
            if len(tokens) == 4 and tokens[0] == "implementation":
                if "$" in tokens[3]:
                    version = self.variables.get(tokens[3].replace('$', ''))
                    return Library(tokens[1], tokens[2], version)
                return Library(tokens[1], tokens[2], tokens[3])

        return None

    def __add_lib(self, lib: Library):
        groups = [g for g in self.lib_groups if g.group_name == lib.group]
        if len(groups) > 0:
            groups[0].add_library(lib)
        else:
            group = LibraryGroup(lib.group)
            group.add_library(lib)
            self.lib_groups.add(group)

    def __check_for_variable(self, line: string) -> Variable | None:
        if "val" in line or "var" in line:
            tokens = (line.replace("val", "")
                      .replace("var", "")
                      .replace(' ', '')
                      .replace('"', '')
                      .replace('\n', '')
                      .split("="))
            return Variable(tokens[0], tokens[1])
        else:
            return None
