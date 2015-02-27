from tkinter import *
from tkinter import ttk, filedialog, messagebox
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

from ea import EA

import threading

class AppUI(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master, relief=SUNKEN, bd=2, highlightthickness=0)
        self.grid(sticky=N+S+E+W)

        self.menubar = Menu(self)
        menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=menu)
        menu.add_command(label="Exit", command=onExit)

        menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Simulator", menu=menu)
        menu.add_command(label="Run", command=lambda: run_pressed(), accelerator="Ctrl+R")
        master.bind("<Control-r>", lambda event: run_pressed())
        menu.add_command(label="Stop", command=lambda: stop_pressed(), accelerator="Ctrl+S")
        master.bind("<Control-s>", lambda event: stop_pressed())

        def run_pressed():
            run_ea()

        def stop_pressed():
            stop_ea()

        try:
            self.master.config(menu=self.menubar)
        except AttributeError:
            self.master.tk.call(master, "config", "-menu", self.menubar)

        #TODO:Temp, Make config file that will alter the program. New stuff should be registered
        options = {
            "genotype": ["default"],
            "translator": ["default", "integer"],
            "parent_selection": ["proportionate", "sigma", "tournament"],
            "adult_selection": ["full", "over", "mixing"],
            "fitness": ["default"]
        }

        self.genotype = LabelledSelect(self, options["genotype"], "Genotype")
        self.genotype.grid(row=2, column=0, sticky=W, padx=4, pady=4)

        self.translator = LabelledSelect(self, options["translator"], "Translator")
        self.translator.grid(row=3, column=0, sticky=W, padx=4, pady=4)

        self.fitness = LabelledSelect(self, options["fitness"], "Fitness evaluator")
        self.fitness.grid(row=4, column=0, sticky=W, padx=4, pady=4)

        self.p_selection = LabelledSelect(self, options["parent_selection"], "Parent selection")
        self.p_selection.grid(row=4, column=0, sticky=W, padx=4, pady=4)

        self.a_selection = LabelledSelect(self, options["adult_selection"], "Adult selection")
        self.a_selection.grid(row=5, column=0, sticky=W, padx=4, pady=4)

        self.population_size = LabelledEntry(self, "Pop size", 20)
        self.population_size.grid(row=0, column=1, padx=4, pady=8)

        self.generations = LabelledEntry(self, "Cycles", 100)
        self.generations.grid(row=0, column=2, padx=4, pady=8)

        self.genome_length = LabelledEntry(self, "Genome length", 20)
        self.genome_length.grid(row=0, column=3, padx=4, pady=8)

        self.average_fitness = Label(self, text="Avg fitness: ")
        self.average_fitness.grid(row=1, column=1, sticky=W ,padx=2, pady=4)
        self.average_fitness_value = Label(self, text="0")
        self.average_fitness_value.grid(row=1, column=1, sticky=E ,padx=2, pady=4)

        self.best_fitness = Label(self, text="Best fitness: ")
        self.best_fitness.grid(row=1, column=2, sticky=W ,padx=2, pady=4)
        self.best_fitness_value = Label(self, text="0")
        self.best_fitness_value.grid(row=1, column=2, sticky=E ,padx=2, pady=4)

        self.progress = ttk.Progressbar(self, orient='horizontal')
        self.progress.grid(row=6, column=0, columnspan=4, sticky="WE")

        self.graph = Graph(self)
        self.graph.grid(row=3, column=1, columnspan=3, rowspan=4)

        self.columnconfigure(0, minsize="150")


    def update(self, p, cf, bf):
        self.progress.step(p)
        self.average_fitness_value.configure(text=str(cf))
        self.best_fitness_value.configure(text=str(bf))

class LabelledSelect(Frame):
    def __init__(self, parent, options, label_text, *args, **kwargs):
        Frame.__init__(self, parent)
        self.label = Label(self, text=label_text)
        self.selected = StringVar(self)
        self.selected.set(options[0])
        self.option_select = OptionMenu(self, self.selected, *options)
        self.option_select.pack(side="bottom", anchor=W)
        self.label.pack(side="top", anchor=W, expand=True)

    def get(self):
        return self.selected.get()


class LabelledEntry(Frame):
    def __init__(self, parent, label_text, default_value,  *args, **kwargs):
        Frame.__init__(self, parent)
        self.label = Label(self, text=label_text)
        self.content = StringVar(self)
        self.content.set(str(default_value))
        self.entry = Entry(self, textvariable=self.content)
        self.entry.pack(side="right", anchor=W)
        self.label.pack(side="left", anchor=W, expand=True)

    def get(self):
        return int(self.content.get())


class Graph(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        label = Label(self, text="Graph Page!")
        label.pack(pady=10,padx=10)


def stop_ea(*args):
    ea_system.stop()


def run_ea(*args):
    ea_system.setup(app.translator.get(),
                 app.fitness.get(),
                 app.genotype.get(),
                 app.a_selection.get(),
                 app.p_selection.get(),
                 app.genome_length.get())

    def callback():
        pop_size = app.population_size.get()
        gen = app.generations.get()
        ea_system.run(pop_size, gen, 1.0)
        app.progress.stop()
    t = threading.Thread(target=callback)
    t.daemon = True
    t.start()


def onExit(*args):
        print("TEST_EXIT")
        root.quit()


root = Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.title("EA problem solver system")
app = AppUI(root)
root.bind('<Return>', run_ea)
ea_system = EA()
ea_system.add_listener(app)

root.mainloop()