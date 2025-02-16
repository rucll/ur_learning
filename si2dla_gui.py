from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
from ast import literal_eval
from si2dla_mod import *
import graphviz
from PIL import ImageTk, Image
import re

import os
import pathlib

os.environ["PATH"] += os.pathsep + f"{pathlib.Path(__file__).parent.resolve()}/graphviz-bin"

global_image_list = []
# check for invalid input

def read_data(D_value):
    if bool(re.match(r"\[(\s*\(\s*(\"|\')[^\"\'\[\]]+(\"|\')\s*,\s*(\"|\')[^\"\'\[\]]+(\"|\')\s*\)\s*,)*\s*(\s*\(\s*(\"|\')[^\"\'\[\]]+(\"|\')\s*,\s*(\"|\')[^\"\'\[\]]+(\"|\')\s*\)\s*,?)\]\s*", D_value)):
        D_list = literal_eval(D_value)
    elif bool(re.match(r"(([^,\s])+,(\s*[^,\s])+\n)*(([^,\s])+,(\s*[^,\s])+)\s*", D_value)):
        lines = D_value.splitlines()
        D_list = []
        for l in lines:
            D_list.append(tuple(l.replace(" ", "").split(",")))
    else:
        return []
    
    return D_list

def read_alphabet(value, D_list):   
    if value == "r_empty":
        strs = []
        for tup in D_list:
            strs.append(tup[0])
        return_list = list(set("".join(strs)))
    elif value == "s_empty":
        strs = []
        for tup in D_list:
            strs.append(tup[1])
        return_list = list(set("".join(strs)))
    elif bool(re.match(r"\[(\s*[\"|\']([^\'\"\[\]])+[\"|\'],)*\s*(\s*[\"|\']([^\'\"\[\]])+[\"|\'])\s*\]\s*", value)):
        return_list = literal_eval(value)
    elif bool(re.match(r"(\s*([^\'\"\[\]\s])+\s*,)*\s*([^\'\"\[\]\s])+\s*", value)):
        return_list = value.replace(" ", "").split(",")
    else: 
        return []

    return return_list

def execute():
    D_value= D_entry.get("1.0", "end-1c")
    R_value = R_entry.get("1.0", "end-1c")
    S_value = S_entry.get("1.0", "end-1c")

    D_list = read_data(D_value)
    
    if D_list == []:
        print("error reading data.")
        return

    execute_algorithm(D_list, R_value, S_value)

def file_execute():
    file_path = filedialog.askopenfilename(title="Select a file:", filetypes=[("Text file", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            file_data = file.read()
            D_list = read_data(file_data)
            if D_list == []:
                print("error reading data.")
                return
        execute_algorithm(D_list, "r_empty", "s_empty")

def execute_algorithm(D_list, R_value, S_value):
    if R_value == "":
        R_value = "r_empty"
    if S_value == "":
        S_value = "s_empty"

    R_list = read_alphabet(R_value, D_list)
    S_list = read_alphabet(S_value, D_list)

    if D_list == []:
        print("error reading data.")
        return
    if R_list == [] or S_list == []:
        print("error reading alphabets.")
        return

    (T_f, T_g) = si2dla(D_list, R_list, S_list)

    graph_f = graphviz.Digraph('graph_f', node_attr={'shape': 'circle', 'fontname': 'Times-Roman', 'fontsize': '12pt', 'fillcolor': 'gray90'}, edge_attr={'fontname': 'Times-Roman', 'fontsize': '12pt', 'penwidth': '0.6', 'arrowsize': '0.6'}, graph_attr={'rankdir': 'LR', 'center': 'true'})
    graph_g = graphviz.Digraph('graph_g', node_attr={'shape': 'circle', 'fontname': 'Times-Roman', 'fontsize': '12pt', 'fillcolor': 'gray90'}, edge_attr={'fontname': 'Times-Roman', 'fontsize': '12pt', 'penwidth': '0.6', 'arrowsize': '0.6'}, graph_attr={'rankdir': 'LR', 'center': 'true'})

    for s in T_f.Q:
        graph_f.node(s)
    for s in T_g.Q:
        graph_g.node(s)


    if len(T_f.Q) == 1:
        e1 = None
        for e in T_f.E:
            if e1 is None:
                e1 = (e[0], e[3])
                e1_label = e[1] + ": " + e[2] + "\\n"
            elif (e[0], e[3]) == e1:
                e1_label = e1_label + e[1] + ": " + e[2] + "\\n"
            else: 
                print("error edge drawing T_f.")
                return

        graph_f.edge(e1[0], e1[1], label=e1_label)


    if len(T_g.Q) == 2:
        e1 = None
        e1_label = ""
        e2 = None
        e2_label = ""
        e3 = None
        e3_label = ""
        e4 = None
        e4_label = ""
        for e in T_g.E:
            if (e[0], e[3]) == e1:
                e1_label = e1_label + e[1] + ": " + e[2] + "\\n"
            elif (e[0], e[3]) == e2:
                e2_label = e2_label + e[1] + ": " + e[2] + "\\n"
            elif (e[0], e[3]) == e3:
                e3_label = e3_label + e[1] + ": " + e[2] + "\\n"
            elif (e[0], e[3]) == e4:
                e4_label = e4_label + e[1] + ": " + e[2] + "\\n"
            elif e1 is None:
                e1 = (e[0], e[3])
                e1_label = e[1] + ": " + e[2] + "\\n"
            elif e2 is None:
                e2 = (e[0], e[3])
                e2_label = e[1] + ": " + e[2] + "\\n"
            elif e3 is None:
                e3 = (e[0], e[3])
                e3_label = e[1] + ": " + e[2] + "\\n"
            elif e4 is None:
                e4 = (e[0], e[3])
                e4_label = e[1] + ": " + e[2] + "\\n"
            else: 
                print("error edge drawing T_g.")
                return


        graph_g.edge(e1[0], e1[1], label=e1_label+"\\n")
        graph_g.edge(e2[0], e2[1], label=e2_label+"\\n")
        graph_g.edge(e3[0], e3[1], label=e3_label+"\\n")
        graph_g.edge(e4[0], e4[1], label=e4_label+"\\n")

        graph_f.format = 'png'
        graph_g.format = 'png'
        
        graph_f.render(directory='gui_files', filename='graph_f').replace('\\', '/')
        graph_g.render(directory='gui_files', filename='graph_g').replace('\\', '/')

        root_dir = pathlib.Path(__file__).resolve().parent

        img_f = ImageTk.PhotoImage(Image.open(root_dir / "gui_files/graph_f.png"))
        global_image_list.append(img_f)
        imglabel_f = Label(mainframe, image=img_f)
        imglabel_f.grid(column=2, row=2, padx=16)
        
        img_g = ImageTk.PhotoImage(Image.open(root_dir / "gui_files/graph_g.png"))
        global_image_list.append(img_g)
        imglabel_g = Label(mainframe, image=img_g)
        imglabel_g.grid(column=3, row=2, padx=16)


        

root = Tk()
root.title("Si2dla Algorithm")
root.resizable(False, False)

mainframe = ttk.Frame(root, padding="25 25 25 20")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

D_label=Label(mainframe, text="insert data here (D):", anchor='sw', width=58)
D_label.grid(column=1, row=1)

D_entry = scrolledtext.ScrolledText(mainframe, width=48, height=15)
D_entry.grid(column=1, row=2, pady=16)

R_label=Label(mainframe, text="insert input alphabet here (Rho):", anchor='sw', width=58)
R_label.grid(column=1, row=3)

R_entry = Text(mainframe, width=50, height=3)
R_entry.grid(column=1, row=4, pady=16)

S_label=Label(mainframe, text="insert output alphabet here (Sigma):", anchor='sw', width=58)
S_label.grid(column=1, row=5)

S_entry = Text(mainframe, width=50, height=3)
S_entry.grid(column=1, row=6, pady=16)

button = Button(mainframe, text="execute", command=execute)
button.grid(column=1, row=9, pady=16)

file_button = Button(mainframe, text="upload text file", command=file_execute)
file_button.grid(column=1, row=10, pady=32)

root.mainloop()