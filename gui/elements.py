from tkinter import *
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import style
style.use('ggplot')

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

class ConfigurationDialog(object):
    def __init__(self, parent, config):

        top = self.top = Toplevel(parent)
        top.title("EA solver - Configuration")
        panes = ttk.Notebook(top)
        panes.pack()
        param = "parameters"
        self.result = None
        self.config = config
        self.elements = config.copy()
        for module_name, module in config.items():
            sub = Frame(panes)
            panes.add(sub, text=module_name)
            for element_name, element in module.items():
                if param in element:
                    t = element[param]
                    header = Label(sub, text=element_name,font=("Helvatica", 10, "bold"))
                    header.pack(padx=5, anchor=W)
                    for i in t.keys():
                        self.elements[module_name][element_name][param][i] = LabelledEntry(sub, i, t[i])
                        self.elements[module_name][element_name][param][i].pack(padx=5, fill="both")


        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5)

    def ok(self):
        self.update()
        self.result = self.config
        self.top.destroy()

    def update(self):
        param = "parameters"
        for module_name, module in self.config.items():
            for element_name, element in module.items():
                if param in element:
                    t = element[param]
                    for i in t.keys():
                        e = self.elements[module_name][element_name][param][i].get()
                        self.config[module_name][element_name][param][i] = e

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
        if self._is_int(v):
            return int(v)
        elif self._is_float(v):
            return float(v)
        elif v == 'True' or v == 'False':
            return eval(v)
        else:
            raise RuntimeError(v + ". Not a number!")

    def get_special(self):
        v = self.content.get()
        if not len(v)>0:
            return float("inf")
        else:
            return self.get()

    def _is_float(self, n):
        try:
            float(n)
            return True
        except ValueError:
            return False

    def _is_int(self, n):
        try:
            int(n)
            return True
        except ValueError:
            return False
