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
import cProfile

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
        menu.add_command(label="Settings", command=lambda: open_configuration(), accelerator="Ctrl+A")
        master.bind("<Control-a>", lambda event: open_configuration())
        menu.add_command(label="Run", command=lambda: run_pressed(), accelerator="Ctrl+R")
        master.bind("<Control-r>", lambda event: run_pressed())
        menu.add_command(label="Stop", command=lambda: stop_pressed(), accelerator="Ctrl+S")
        master.bind("<Control-s>", lambda event: stop_pressed())

        options = Configuration.get()
        def run_pressed():
            run_ea()

        def stop_pressed():
            stop_ea()

        def open_configuration():
            d = ConfigurationDialog(master, options)
            master.wait_window(d.top)
            value = d.result
            print(value)
            #Save configuration
        try:
            self.master.config(menu=self.menubar)
        except AttributeError:
            self.master.tk.call(master, "config", "-menu", self.menubar)

        gui_control_elements = [
            {"name": "population_size", "label": "Pop size", "value": 20},
            {"name": "generations","label": "Cycles", "value": 100},
            {"name": "genome_length", "label": "Genome length", "value": 20},
            {"name": "threshold", "label": "Threshold","value": 1},
            {"name": "genotype", "label": "Genotype","value": None},
            {"name": "translator", "label": "Translator","value": None},
            {"name": "fitness", "label": "Fitness","value": None},
            {"name": "parent_selection", "label": "Parent selection","value": None},
            {"name": "adult_selection", "label": "Adult selection","value": None},
            ]

        self.elements = {}
        for i in range(4):
            e = gui_control_elements[i]
            self.elements[e["name"]] = LabelledEntry(self, e["label"], e["value"])
            self.elements[e["name"]].grid(row=i+1, column=0, padx=4, pady=4, sticky="WE")
            self.rowconfigure(i+1,weight=1)

        for i in range(4,len(gui_control_elements)):
            e = gui_control_elements[i]
            self.elements[e["name"]] = LabelledSelect(self, self.option_list(options[e["name"]]), e["label"])
            self.elements[e["name"]].grid(row=i+1, column=0, padx=4, pady=4, sticky="WE")
            self.rowconfigure(i+1,weight=1)

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

    def option_list(self, d):
        return sorted(d, key=lambda k: d[k]["order"])

    def update(self, c, p, cf, bf, std):
        self.progress.step(p)
        self.average_fitness_value.configure(text=str("%.3f" %cf))
        self.best_fitness_value.configure(text=str("%.3f" %bf))
        self.cycles_value.configure(text=str(c))
        self.graph.add(c, bf, cf, std)

class ConfigurationDialog(object):
    def __init__(self, parent, config):

        top = self.top = Toplevel(parent)
        #Todo: Make good configuration popup
        #Maybe use panes for each module of the eA
        Label(top, text="Configuration").pack()
        for module_name, module in config.items():
            for element_name, element in module.items():
                if "parameters" in element:
                    t = element["parameters"]
                    header = Label(top, text=element_name)
                    header.pack(padx=5)
                    for i in t.keys():
                        lab = LabelledEntry(top, i, t[i])
                        lab.pack(padx=5)

        self.config = config
        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5)

    def ok(self):
        self.result = self.config
        self.top.destroy()

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
    ea_system.setup(app.elements["translator"].get(),
                 app.elements["fitness"].get(),
                 app.elements["genotype"].get(),
                 app.elements["adult_selection"].get(),
                 app.elements["parent_selection"].get(),
                 app.elements["genome_length"].get())
    app.graph.clear()

    def callback():
        pop_size = int(app.elements["population_size"].get())
        gen = int(app.elements["generations"].get())
        threshold = app.elements["threshold"].get_special()
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
