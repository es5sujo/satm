import json
import os.path


class JsonManifest:
    def __init__(self, language: str):
        self.file = None
        self.translations = None
        self.keys = None
        self.language = language
    
    def loadManifest(self, path: str):
        if not os.path.isfile(path):
            raise Exception(f"Could not file {path}")
        self.file = path
        file_handle = open(self.file, "r")
        file_data = file_handle.read()
        translations = json.loads(file_data)
        self.translations = translations
        self.updateKeys()
    
    def compare(self, other):
        return (self.keys - other.keys, other.keys - self.keys)
    
    def updateTerm(self, term: str, value: str):
        if type(value) != str:
            return
        
        if value == "":
            del self.translations[term]
        else:
            self.translations[term] = value

        self.updateKeys()
        print(self.translations)
    
    def deleteTerm(self, term: str):
        if term in self.translations:
            del self.translations[term]
            self.updateKeys()
            print(self.translations)
    
    def updateKeys(self):
        self.keys = set(self.translations.keys())
