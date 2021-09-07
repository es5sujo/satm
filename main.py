from GUI import create_interface
from TranslatedProject import TranslatedProject
from JsonManifest import JsonManifest
import json

en = JsonManifest("en")
en.loadManifest("demo/appl1/en.json")

sv = JsonManifest("sv")
sv.loadManifest("demo/appl1/sv.json")

projects = [
    TranslatedProject("New project", "demo/")
]
projects[0].addTranslation(sv)
projects[0].addTranslation(en)

create_interface(set.union(en.keys, sv.keys), projects)

print(json.dumps(projects[0].toJson()))