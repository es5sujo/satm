from JsonManifest import JsonManifest

class TranslatedProject:

    def __init__(self, name, basePath):
        self.name = name
        self.basePath = basePath
        self.translations = {}
        self._newTerms = []
        self.changes = 0
    
    def addTranslation(self, translation: JsonManifest):
        self.translations[translation.language] = translation
    
    def getTermTranslations(self, term):
        output = {}
        for lang, manifest in self.translations.items():
            try:
                output[manifest.language] = manifest.translations[term]
            except:
                output[manifest.language] = ""
        
        return output
    
    def getMissingLanguages(self, term):
        terms = self.getTermTranslations(term)
        langs = []
        for lang in terms:
            if terms[lang] == "":
                langs.append(lang)
        
        return langs

    def getKeys(self):
        keys = set()
        for language, manifest in self.translations.items():
            keys = set.union(keys, manifest.keys)
        keys = set.union(keys, self._newTerms)
        return sorted(keys)
    
    def updateTerm(self, lang: str, term: str, value: str):
        if term in self._newTerms:
            self._newTerms.remove(term)

        if not lang in self.translations:
            print(f"TranslatedProject::updateTerm: Can not find language {lang}")
            return
        
        self.changes = self.changes + 1
        self.translations[lang].updateTerm(term, value)
    
    def createTerm(self, term: str):
        self._newTerms.append(term)
    
    def deleteTerm(self, term: str):
        terms = self.getKeys()
        if not term in terms:
            return
        
        if term in self._newTerms:
            self._newTerms.remove(term)
        
        for language, obj in self.translations.items():
            obj.deleteTerm(term)

    def getChanges(self):
        return self.changes
    
    def toJson(self):
        translations = {}
        for lang, translation in self.translations.items():
            translations[lang] = translation.toJson()

        return {
            "name": self.name,
            "translations": translations
        }
