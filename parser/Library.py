import string


class Library:
    def __init__(self, group: string, name: string, version: string):
        self.version = version
        self.name = name
        self.group = group

    def __str__(self):
        return "lib: " + self.group + " " + self.name + " " + self.version

    def __eq__(self, other):
        return self.group == other.group and self.name == other.name

    def __hash__(self):
        return hash((self.group, self.name))
