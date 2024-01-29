import string

from parser.LibraryGroup import LibraryGroup


class VersionCatalogGenerator:
    libs_version_catalog = None

    def __init__(self, lib_groups: [LibraryGroup], directory_to_save: string, file_name: string):
        self.lib_groups = lib_groups
        self.directory_to_save = directory_to_save
        self.file_name = file_name

    def generate(self):
        self.libs_version_catalog = open(self.directory_to_save + "\\" + self.file_name + ".toml", "w")
        self.__write_versions()
        self.libs_version_catalog.write("\n")
        self.__write_libraries()

    def __write_versions(self):
        self.libs_version_catalog.write("[versions]\n")
        for lib_group in self.lib_groups:
            v_name = self.__get_version_name(lib_group.group_name)
            self.libs_version_catalog.write(v_name + " = " + "\"" + lib_group.version + "\"\n")

    def __write_libraries(self):
        self.libs_version_catalog.write("[libraries]\n")
        for lib_group in self.lib_groups:
            for lib in lib_group.libs:
                self.libs_version_catalog.write(
                    lib.name
                    + " = { id = \""
                    + lib.group
                    + "\", name = \""
                    + lib.name
                    + "\", version.ref = \""
                    + self.__get_version_name(lib.group)
                    + "\" }\n"
                )

    def __get_version_name(self, group_name: string) -> string:
        return group_name.split('.')[-1]
