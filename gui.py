from tkinter import *
from tkinter import ttk, filedialog, messagebox
from configuration import Configuration
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
style.use('ggplot')
import sys

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

        options = Configuration.get()
        self.population_size = LabelledEntry(self, "Pop size", 20)
        self.population_size.grid(row=1, column=0, padx=4, pady=4, sticky="WE")

        self.generations = LabelledEntry(self, "Cycles", 100)
        self.generations.grid(row=2, column=0, padx=4, pady=4, sticky="WE")

        self.genome_length = LabelledEntry(self, "Genome length", 20)
        self.genome_length.grid(row=3, column=0, padx=4, pady=4, sticky="WE")

        self.threshold = LabelledEntry(self, "Threshold", 1)
        self.threshold.grid(row=4, column=0, padx=4, pady=4, sticky="WE")

        self.genotype = LabelledSelect(self, self.option_list(options["genotype"]), "Genotype")
        self.genotype.grid(row=5, column=0, padx=4, pady=4, sticky="WE")

        self.translator = LabelledSelect(self, self.option_list(options["translator"]), "Translator")
        self.translator.grid(row=6, column=0, padx=4, pady=4, sticky="WE")

        self.fitness = LabelledSelect(self, self.option_list(options["fitness"]), "Fitness evaluator")
        self.fitness.grid(row=7, column=0, padx=4, pady=4, sticky="WE")

        self.p_selection = LabelledSelect(self, self.option_list(options["parent_selection"]), "Parent selection")
        self.p_selection.grid(row=8, column=0,  padx=4, pady=4, sticky="WE")

        self.a_selection = LabelledSelect(self, self.option_list(options["adult_selection"]), "Adult selection")
        self.a_selection.grid(row=9, column=0,  padx=4, pady=4, sticky="WE")



        self.average_fitness = Label(self, text="Avg fitness: ")
        self.average_fitness.grid(row=0, column=1, sticky=W ,padx=2, pady=4)
        self.average_fitness_value = Label(self, text="0")
        self.average_fitness_value.grid(row=0, column=1, sticky=E ,padx=2, pady=4)

        self.best_fitness = Label(self, text="Best fitness: ")
        self.best_fitness.grid(row=0, column=2, sticky=W ,padx=2, pady=4)
        self.best_fitness_value = Label(self, text="0")
        self.best_fitness_value.grid(row=0, column=2, sticky=E ,padx=2, pady=4)

        self.cycles = Label(self, text="Cycles: ")
        self.cycles.grid(row=0, column=3, sticky=W ,padx=2, pady=4)
        self.cycles_value = Label(self, text="0")
        self.cycles_value.grid(row=0, column=3, sticky=E ,padx=2, pady=4)

        self.progress = ttk.Progressbar(self, orient='horizontal')
        self.progress.grid(row=10, column=0, columnspan=5, sticky="WES")

        self.graph = Graph(self)
        self.graph.grid(row=1, column=1, columnspan=4, rowspan=9, sticky="WNSE")

        self.columnconfigure(0, minsize="150")
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight=1)
        self.rowconfigure(3,weight=1)
        self.rowconfigure(4,weight=1)
        self.rowconfigure(5,weight=1)
        self.rowconfigure(6,weight=1)
        self.rowconfigure(7,weight=1)
        self.rowconfigure(8,weight=1)

    def option_list(self, d):
        return sorted(d, key=lambda k: d[k]["order"])

    def update(self, c, p, cf, bf, std):
        self.progress.step(p)
        self.average_fitness_value.configure(text=str(cf))
        self.best_fitness_value.configure(text=str(bf))
        self.cycles_value.configure(text=str(c))
        self.graph.add(c, bf, cf, std)

class LabelledSelect(Frame):
    def __init__(self, parent, options, label_text, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.label = Label(self, text=label_text)
        self.selected = StringVar(self)
        self.selected.set(options[0])
        self.option_select = OptionMenu(self, self.selected, *options)
        self.option_select.pack(side="right", anchor=E)
        self.label.pack(side="left", anchor=W, expand=True)

    def get(self):
        return self.selected.get()


class LabelledEntry(Frame):
    def __init__(self, parent, label_text, default_value,  *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.label = Label(self, text=label_text)
        self.content = StringVar(self)
        self.content.set(str(default_value))
        self.entry = Entry(self, textvariable=self.content)
        self.label.pack(side="left", anchor=W, expand=True)
        self.entry.pack(side="right", anchor=E)

    def get(self):
        v = self.content.get()
        if self._is_number(v):
            return float(v)
        else:
            raise RuntimeError("Not a number!")

    def get_special(self):
        v = self.content.get()
        if not len(v)>0:
            return float("inf")
        else:
            return self.get()

    def _is_number(self, n):
        try:
            float(n)
            return True
        except ValueError:
            return False

class Graph(Frame):
    #TODO: Clean up code

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.f = Figure()
        self.a = self.f.add_subplot(211)
        self.b = self.f.add_subplot(212)
        self.x_list = []
        self.bf_list = []
        self.af_list = []
        self.std_list = []

        canvas = FigureCanvasTkAgg(self.f, self)
        canvas._tkcanvas.config(highlightthickness=0)
        canvas.show()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)

    def add(self, x, bf, af, std):
        self.x_list.append(x)
        self.bf_list.append(bf)
        self.af_list.append(af)
        self.std_list.append(std)

    def animate(self, i):
        self.a.clear()
        self.b.clear()
        self.a.plot(self.x_list, self.bf_list, label="Best")
        self.a.plot(self.x_list, self.af_list, label="Average")
        self.b.plot(self.x_list, self.std_list, label="Std")
        self.a.legend( loc='lower right' )
        self.b.legend( loc='upper right' )

    def clear(self):
        self.x_list = []
        self.bf_list = []
        self.af_list = []
        self.std_list = []


def stop_ea(*args):
    ea_system.stop()


def run_ea(*args):
    ea_system.setup(app.translator.get(),
                 app.fitness.get(),
                 app.genotype.get(),
                 app.a_selection.get(),
                 app.p_selection.get(),
                 app.genome_length.get())
    app.graph.clear()

    def callback():
        pop_size = int(app.population_size.get())
        gen = int(app.generations.get())
        threshold = app.threshold.get_special()
        ea_system.run(pop_size, gen, threshold)
        app.progress.stop()
    t = threading.Thread(target=callback)
    t.daemon = True
    t.start()



def onExit(*args):
        print("TEST_EXIT")
        root.quit()


Configuration.init()
root = Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.title("EA problem solver system")
app = AppUI(root)
root.bind('<Return>', run_ea)
ea_system = EA()
ani = animation.FuncAnimation(app.graph.f, app.graph.animate, interval=1000)
ea_system.add_listener(app)
root.mainloop()
