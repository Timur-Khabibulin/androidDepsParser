from parser.Parser import Parser
from VersionCatalogGenerator import VersionCatalogGenerator

project_path = input("Enter a path to the project: ")
version_catalog_file_name = input("Enter the name of the .toml file to be created: ")
print(version_catalog_file_name + " will be saved in " + project_path)

lib_groups = Parser().get_libraries(project_path)

VersionCatalogGenerator(
    lib_groups,
    project_path,
    version_catalog_file_name
).generate()

print("The file was successfully generated")
