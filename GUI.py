from typing import List
from GUITermEditor import TermEditor
from JsonManifest import JsonManifest
from TranslatedProject import TranslatedProject
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
import tkinter
from PIL import Image, ImageTk

from GUIImportWizard import ImportWizard

class ProjectViewer:
    def __init__(self, parent, on_change):
        self.on_change = on_change

        explorer = ttk.Treeview(parent, show="tree")
        self.object = explorer
        explorer.grid(column=0, row=0, sticky=(N, W, E, S), columnspan=1)
        explorer.columnconfigure(0, weight=1)
        explorer.rowconfigure(0, weight=1)
        explorer.bind("<<TreeviewSelect>>", self._on_change)

        self._loadImages()
    
    def _loadImages(self):
        bullet_path = "./icons/bullet_black.png"
        self.bullet_img = ImageTk.PhotoImage(Image.open(bullet_path))

    def setEntries(self, entries):
        for v in entries:
            self.object.insert("", END, v, text=v, image=self.bullet_img)
    
    def _on_change(self, *args):
        selected_term = self.object.selection()[0]
        print(self.on_change)
        self.on_change(selected_term)

    def log(self, *args):
        print(self, args)
        print(self.object.selection()[0])

class ProjectViewer2(tkinter.Frame):
    def __init__(self, parent, projects, callbacks):
        super(ProjectViewer2, self).__init__()

        self.projects = projects

        self._loadImages()
        if type(callbacks) == dict:
            self.callbacks = callbacks
        else:
            print("ProjectViewer2: Found no callbacks")
            self.callbacks = {}

        self.treeView = ttk.Treeview(self, show="tree")
        self.treeView.grid(column=0, row=1, columnspan=6, sticky=(N, S, E, W))
        self.treeView.bind("<<TreeviewSelect>>", self._on_change)

        self.newButton = ttk.Button(self, image=self.images["page_add"], command=self._on_add)
        self.newButton.grid(column=0, row=0, sticky=(N, S, E, W))
        self.saveButton = ttk.Button(self, image=self.images["disk"])
        self.saveButton.grid(column=1, row=0, sticky=(N, S, E, W))
        self.loadButton = ttk.Button(self, image=self.images["folder"])
        self.loadButton.grid(column=2, row=0, sticky=(N, S, E, W))
        self.addButton = ttk.Button(self, image=self.images["add"], command=self._on_term_add)
        self.addButton.grid(column=3, row=0, sticky=(N, S, E, W))
        self.deleteButton = ttk.Button(self, image=self.images["delete"], command=self._on_term_delete)
        self.deleteButton.grid(column=4, row=0, sticky=(N, S, E, W))
        self.findButton = ttk.Button(self, image=self.images["find"])
        self.findButton.grid(column=5, row=0, sticky=(N, S, E, W))

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)

        self._renderTreeOptions()
    
    def _loadImages(self):
        self.images = {}
        self.images["add"] = ImageTk.PhotoImage(Image.open("./icons/add.png"))
        self.images["application_add"] = ImageTk.PhotoImage(Image.open("./icons/application_add.png"))
        self.images["bullet_green"] = ImageTk.PhotoImage(Image.open("./icons/bullet_green.png"))
        self.images["bullet_red"] = ImageTk.PhotoImage(Image.open("./icons/bullet_red.png"))
        self.images["bullet_yellow"] = ImageTk.PhotoImage(Image.open("./icons/bullet_yellow.png"))
        self.images["delete"] = ImageTk.PhotoImage(Image.open("./icons/delete.png"))
        self.images["disk"] = ImageTk.PhotoImage(Image.open("./icons/disk.png"))
        self.images["find"] = ImageTk.PhotoImage(Image.open("./icons/find.png"))
        self.images["folder"] = ImageTk.PhotoImage(Image.open("./icons/folder.png"))
        self.images["page_add"] = ImageTk.PhotoImage(Image.open("./icons/page_add.png"))
    
    def setSelectedIcon(self, project):
        focused = self.treeView.focus()
        item_id = self.treeView.index(focused)
        parent_id = self.treeView.parent(focused)
        text = focused.replace("Term:", "")
        self.treeView.delete(focused)
        image = self.images["bullet_green"]
        missing_langs = project.getMissingLanguages(text)
        if len(missing_langs) == len(project.translations.keys()):
            image = self.images["bullet_red"]
        elif len(missing_langs) > 0:
            image = self.images["bullet_yellow"]
        newRow = self.treeView.insert(parent_id, item_id, focused, text=text, image=image)
        self.treeView.focus(newRow)

    def setProjects(self, projects):
        print(projects)
        if type(projects) != list:
            return
        self.projects = projects
        self._clearTree()
        self._renderTreeOptions()
    
    def _clearTree(self):
        self.treeView.delete(*self.treeView.get_children())

    def _renderTreeOptions(self):
        for project in self.projects:
            parent_id = self.treeView.insert("", END, f"Project:{project.name}", text=project.name, open=True)
            parent_index = self.treeView.index(parent_id)
            for term in project.getKeys():
                image = self.images["bullet_green"]
                if len(project.getMissingLanguages(term)) > 0:
                    image = self.images["bullet_yellow"]
                self.treeView.insert(parent_id, END, f"Term:{term}", text=term, image=image)
    
    def _on_add(self, *args):
        newFiles = filedialog.askopenfilenames(title="Open language manifest...", filetypes=[("JSON", "*.json")])
        if "add_manifest" in self.callbacks and callable(self.callbacks["add_manifest"]):
            self.callbacks["add_manifest"](newFiles)
        else:
            print("ProjectViewer2: Found no callback for add_manifest")
        
    def _on_change(self, *args):
        selected_term = self.treeView.selection()[0].replace("Term:", "")
        project = self.treeView.parent(self.treeView.selection()[0]).replace("Project:", "")
        print(project, selected_term)
        if not selected_term.startswith("Project:"):
            if "select_term" in self.callbacks and callable(self.callbacks["select_term"]):
                self.callbacks["select_term"](project, selected_term)
            else:
                print("ProjectViewer2: Found no callback for select_term")
    
    def _on_term_add(self):
        try:
            project = self.treeView.selection()[0]
            if not project.startswith("Project:"):
                project = self.treeView.parent(project)
                if not project.startswith("Project:"):
                    print("ProjectViewer2: Could not find a selected project")
                    return
            project = project.replace("Project:", "")
            if "add_term" in self.callbacks and callable(self.callbacks["add_term"]):
                self.callbacks["add_term"](project)
            else:
                print("ProjectViewer2: Found no callback for add_term")
        except IndexError:
            messagebox.showinfo(message="You must select an application to create a new language term")
        
    def _on_term_delete(self):
        try:
            for term in self.treeView.selection():
                if not term.startswith("Term:"):
                    print("ProjectViewer2: Could not get the highlighted term")
                    return
                project = self.treeView.parent(term)
                if not project.startswith("Project:"):
                    print("ProjectViewer2: Could not get the selected project for term deletion")
                    return
                term = term.replace("Term:", "")
                project = project.replace("Project:", "")
                if "delete_term" in self.callbacks and callable(self.callbacks["delete_term"]):
                    self.callbacks["delete_term"](project, term)
                else:
                    print("ProjectViewer2: Found no callback for delete_term")
        except IndexError:
            messagebox.showinfo(message="You must select a term in order to delete it")

def create_interface(entries, projects: List[TranslatedProject]):
    def handle_select(project, term):
        id = get_project_index(project)
        terms = projects[id].getTermTranslations(term)
        termEditor.setTerms(terms, term, project)

    def handle_edit(project, lang, term, val):
        id = get_project_index(project)
        projects[id].updateTerm(lang, term, val)
        projectViewer.setSelectedIcon(projects[id])
    
    def handle_new_file(files):
        wizard = ImportWizard(files)

    def handle_new_term(project):
        print(project)
        term = simpledialog.askstring("Add new language term...", "Enter new language term")
        if term == None:
            return

        id = get_project_index(project)
        projects[id].createTerm(term)
        projectViewer.setProjects(projects)
    
    def handle_delete_term(project, term):
        print(project, term)
        id = get_project_index(project)
        projects[id].deleteTerm(term)
        projectViewer.setProjects(projects)
    
    def get_project_index(project):
        for i in range(len(projects)):
            print(i)
            if projects[i].name == project:
                return i

    root = Tk()
    root.title("Language Editor")
    root.geometry("800x600")
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=9)
    root.rowconfigure(0, weight=0)
    root.rowconfigure(1, weight=1)

    projectViewer = ProjectViewer2(root, projects, {
        "add_manifest": handle_new_file,
        "add_term": handle_new_term,
        "delete_term": handle_delete_term,
        "select_term": handle_select
    })
    projectViewer.grid(column=0, row=1, sticky=(N, W, S, E))

    termEditor = TermEditor(root, {
        "edit_term": handle_edit
    })
    termEditor.grid(column=1, row=1, sticky=(N, W, S, E), padx=(20, 20), pady=(20, 20))

    termEditor.columnconfigure(0, weight=1)

    root.mainloop()