from tkinter import *
from tkinter import ttk
import tkinter

class TermEditor(tkinter.Frame):
    def __init__(self, parent, callbacks):
        super(TermEditor, self).__init__()
        self.terms = {}
        self.term = ""
        self.project = ""
        self.fields = {}
        self.label = Label(self, text="No translation selected")
        self.label.grid(column=0, row=0, sticky=(N))
        self._drawTerms()
        
        if type(callbacks) == dict:
            self.callbacks = callbacks
        else:
            print("TermEditor: Found no callbacks")
            self.callbacks = {}
    
    def setTerms(self, terms, term, project: str):
        self.terms = terms
        self.term = term
        self.project = project
        self.label.config(text=f"{term[:20]}")
        self._drawTerms()
    
    def getSelectedProject(self):
        return self.project

    def _drawTerms(self):
        for lang, props in self.fields.items():
            props["field"].destroy()
            props["label"].destroy()
        
        self.fields = {}
        if type(self.terms) != dict:
            return
        
        for lang, v in self.terms.items():
            var = StringVar(self, v, lang)
            props = {
                "label": ttk.Label(self, text=lang),
                "var": var,
                "field": ttk.Entry(self, textvariable=var)
            }

            props["label"].grid(column=0, row=(len(self.fields) * 2 + 1))
            props["var"].trace_add("write", self._on_change)
            props["field"].grid(column=0, row=(len(self.fields) * 2 + 2), sticky=(N, S, E, W))

            self.fields[lang] = props

    def _drawTermsOld(self):
        print("_drawTerms", self.terms)
        for field in self.termFields:
            field.destroy()
        
        for label in self.termLabels:
            label.destroy()
        
        self.termInputs = list()

        if type(self.terms) != dict:
            return

        for k, v in self.terms.items():

            label = ttk.Label(self, text=k)
            label.grid(column=0, row=(len(self.termFields) * 2))
            var = StringVar(self, v, k)
            var.trace_add("write", self._on_change)
            field = ttk.Entry(self, textvariable=var)
            field.grid(column=0, row=(len(self.termFields) * 2 + 1), sticky=(N, S, E, W))
            self.termLabels.append(label)
            self.termFields.append(field)

            self.termInputs.append(var)

    def _on_change(self, *args):
        lang = args[0]
        val = self.fields[args[0]]["var"].get()
        print(f"{self.term}[{args[0]}] = {val}")
        if "edit_term" in self.callbacks and callable(self.callbacks["edit_term"]):
            self.callbacks["edit_term"](self.project, lang, self.term, val)
        else:
            print("ProjectViewer2: Found no callback for edit_term")