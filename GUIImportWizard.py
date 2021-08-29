from tkinter import *
from tkinter import ttk
import tkinter

class ImportWizard(Tk):
    def __init__(self, filePaths):
        super().__init__()
        self.title(f"Import files")
        #self.geometry("400x400")
        
        self.files = []
        i = 0
        for file in filePaths:
            input = ImportedEntry(self, file)
            input.grid(column=0, row=i, sticky=(N, S, E, W), padx=(10, 10), pady=(10, 10))

            self.files.append(input)
            i = i + 1

        self.columnconfigure(0, weight=1)
        self.mainloop()

class ImportedEntry(Frame):
    def __init__(self, parent, file):
        super(ImportedEntry, self).__init__(parent)
        self.file = file
        self.columnconfigure(0, weight=1)

        self.language = StringVar()
        self.languageLabel = tkinter.Label(self, text=f"Language ({self.file})")
        self.languageLabel.grid(column=0, row=0, sticky=(N, S, W))
        self.languageEntry = tkinter.Entry(self, textvariable=self.language)
        self.languageEntry.grid(column=0, row=1, sticky=(N, S, E, W))

        self.formatLabel = tkinter.Label(self, text="File format")
        self.formatLabel.grid(column=0, row=2, sticky=(N, S, W))
        self.format = ImportedFormatSelector(self)
        self.format.grid(column=0, row=3, sticky=(N, S, W))

class ImportedFormatSelector(OptionMenu):
    def __init__(self, parent):
        self.formats = ("JSON",)
        self.selectedFormat = StringVar()
        self.selectedFormat.set(self.formats[0])
        super(ImportedFormatSelector, self).__init__(parent, self.selectedFormat, self.formats)

