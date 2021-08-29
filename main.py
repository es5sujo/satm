from GUI import create_interface
from TranslatedProject import TranslatedProject
from JsonManifest import JsonManifest

en = JsonManifest("en")
en.loadManifest("demo/en.json")

sv = JsonManifest("sv")
sv.loadManifest("demo/sv.json")

projects = [
    TranslatedProject("New project", "demo/")
]
projects[0].addTranslation(sv)
projects[0].addTranslation(en)

create_interface(set.union(en.keys, sv.keys), projects)