import string

from parser.Library import Library


class LibraryGroup:
    group_name = ""
    version = ""

    def __init__(self, group_name: string):
        self.group_name = group_name
        self.libs = set()
        self.version = ""

    def add_library(self, library: Library):
        self.libs.add(library)
        self.__set_version(library.version)

    def __set_version(self, version: string):
        if self.version == '':
            self.version = version
        else:
            self.version = self.__get_latest_version(version)

    def __get_latest_version(self, version: str) -> string:
        t1 = self.version.split('-')[0].split('.')
        t2 = version.split('-')[0].split('.')
        for i in range(len(t1)):
            try:
                if int(t1[i]) > int(t2[i]):
                    return self.version
                elif int(t1[i]) < int(t2[i]):
                    return version
            except ValueError:
                print("Error when parsing version. Setting default version to 0")
                return "0"

        return self.version

    def __str__(self):
        my_str = "Group: " + self.group_name + " " + self.version + "\n"
        for library in self.libs:
            my_str += "  " + library.__str__() + "\n"

        return my_str

    def __eq__(self, other):
        return self.group_name == other.group_name

    def __hash__(self):
        return hash(self.group_name)
