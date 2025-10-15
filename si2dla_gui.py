from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
from ast import literal_eval
from si2dla_new import *
from domain_inference import infer_domain
import graphviz
from PIL import ImageTk, Image
import re
from data import chandleejardine, huajardine, opacity, deletion
from parser import parse_csv
import os
import pathlib

os.environ["PATH"] += os.pathsep + f"{pathlib.Path(__file__).parent.resolve()}/graphviz-bin"

global_image_list = []
# check for invalid input

# def read_data(D_value):
#     if bool(re.match(r"\[(\s*\(\s*(\"|\')[^\"\'\[\]]*(\"|\')\s*,\s*(\"|\')[^\"\'\[\]]*(\"|\')\s*\)\s*,)*\s*(\s*\(\s*(\"|\')[^\"\'\[\]]*(\"|\')\s*,\s*(\"|\')[^\"\'\[\]]*(\"|\')\s*\)\s*,?)\]\s*", D_value)):
#         D_list = literal_eval(D_value)
#     elif bool(re.match(r"(([^,\s])+,(\s*[^,\s])+\n)*(([^,\s])+,(\s*[^,\s])+)\s*", D_value)):
#         lines = D_value.splitlines()
#         D_list = []
#         for l in lines:
#             D_list.append(tuple(l.replace(" ", "").split(",")))
#     else:
#         return []
    
#     return D_list

def read_alphabet(D_list):   
    R_list = []
    S_list = []
    for data_pair in D_list:
        R_list.extend(data_pair[0])
        S_list.extend(data_pair[1])

    R_list = list(set(R_list))
    S_list = list(set(S_list))
    return (R_list, S_list)

# def read_alphabet(value, D_list):   
#     if value == "r_empty":
#         strs = []
#         for tup in D_list:
#             strs.append(tup[0])
#         return_list = list(set("".join(strs)))
#     elif value == "s_empty":
#         strs = []
#         for tup in D_list:
#             strs.append(tup[1])
#         return_list = list(set("".join(strs)))
#     elif bool(re.match(r"\[(\s*[\"|\']([^\'\"\[\]])+[\"|\'],)*\s*(\s*[\"|\']([^\'\"\[\]])+[\"|\'])\s*\]\s*", value)):
#         return_list = literal_eval(value)
#     elif bool(re.match(r"(\s*([^\'\"\[\]\s])+\s*,)*\s*([^\'\"\[\]\s])+\s*", value)):
#         return_list = value.replace(" ", "").split(",")
#     else: 
#         return []

#     return return_list

# def execute():
#     D_value = D_entry.get("1.0", "end-1c")
#     R_value = R_entry.get("1.0", "end-1c")
#     S_value = S_entry.get("1.0", "end-1c")

#     D_list = read_data(D_value)
    
#     if D_list == []:
#         print("error reading data.")
#         return

#     execute_algorithm(D_list, R_value, S_value)

def file_execute():
    file_path = filedialog.askopenfilename(title="Select a file:", filetypes=[("Text file", "*.csv")])
    print(file_path)
    D_list = parse_csv(file_path)
    execute_algorithm(D_list)

def execute_algorithm(D_list):
    # if R_value == "":
    #     R_value = "r_empty"
    # if S_value == "":
    #     S_value = "s_empty"



    (R_list, S_list) = read_alphabet(D_list)

    if D_list == []:
        print("error reading data.")
        return
    if R_list == [] or S_list == []:
        print("error reading alphabets.")
        return
    
    root.image_frame.pack(pady=20)


    T = infer_domain(D_list)

    (T_f, T_g) = si2dla_ex(T, D_list, R_list, S_list)

    graph_f = graphviz.Digraph('graph_f', node_attr={'shape': 'circle', 'fontname': 'Times-Roman', 'fontsize': '12pt', 'fillcolor': 'gray90'}, edge_attr={'fontname': 'Times-Roman', 'fontsize': '12pt', 'penwidth': '0.6', 'arrowsize': '0.6'}, graph_attr={'rankdir': 'LR', 'center': 'true'})
    graph_g = graphviz.Digraph('graph_g', node_attr={'shape': 'circle', 'fontname': 'Times-Roman', 'fontsize': '12pt', 'fillcolor': 'gray90'}, edge_attr={'fontname': 'Times-Roman', 'fontsize': '12pt', 'penwidth': '0.6', 'arrowsize': '0.6'}, graph_attr={'rankdir': 'LR', 'center': 'true'})
    graph_d = graphviz.Digraph('graph_d', node_attr={'shape': 'circle', 'fontname': 'Times-Roman', 'fontsize': '12pt', 'fillcolor': 'gray90'}, edge_attr={'fontname': 'Times-Roman', 'fontsize': '12pt', 'penwidth': '0.6', 'arrowsize': '0.6'}, graph_attr={'rankdir': 'LR', 'center': 'true'})


    for s in T_f.Q:
        graph_f.node(s)
    for s in T_g.Q:
        graph_g.node(s)
    for s in T.Q:
        s = str(s)
        graph_d.node(s)
        

    if len(T_f.Q) == 1:
        tr_label = ''
        for tr in T_f.E:
            tr_label = tr_label + tr[1] + ": " + ''.join(tr[2]) + '\\n'
        
        graph_f.edge(T_f.Q[0], T_f.Q[0], label=tr_label)


    state_mappings = {}


    for tr in T.E:
        if (tr[0], tr[3]) not in state_mappings:
            state_mappings[(tr[0], tr[3])] = [tr[1]]
        else:
            state_mappings[(tr[0], tr[3])].append(tr[1]) 

    for states, inputs in state_mappings.items():
        tr_label = ''
        for inp in inputs:
            tr_label = tr_label + inp + '\\n'
        
        graph_d.edge(str(states[0]), str(states[1]), label=tr_label)

    state_mappings.clear()

 
    if len(T_g.Q) == 2:
        for tr in T_g.E:
            if (tr[0], tr[3]) not in state_mappings:
                state_mappings[(tr[0], tr[3])] = [tr[1] + ': ' + tr[2]]
            else:
                 state_mappings[(tr[0], tr[3])].append(tr[1] + ': ' + tr[2])
        
        for states, inputs in state_mappings.items():
            tr_label = ''
            for inp in inputs:
                tr_label = tr_label + inp + '\\n'
                
            graph_g.edge(str(states[0]), str(states[1]), label=tr_label)

        state_mappings.clear()

        graph_f.format = 'png'
        graph_g.format = 'png'
        graph_d.format = 'png'
        
        graph_f.render(directory='gui_files', filename='graph_f').replace('\\', '/')
        graph_g.render(directory='gui_files', filename='graph_g').replace('\\', '/')
        graph_d.render(directory='gui_files', filename='graph_d').replace('\\', '/')

        root_dir = pathlib.Path(__file__).resolve().parent

        img_f = ImageTk.PhotoImage(Image.open(root_dir / "gui_files/graph_f.png"))
        global_image_list.append(img_f)
        
        img_g = ImageTk.PhotoImage(Image.open(root_dir / "gui_files/graph_g.png"))
        global_image_list.append(img_g)

        img_d = ImageTk.PhotoImage(Image.open(root_dir / "gui_files/graph_d.png"))
        global_image_list.append(img_d)

        subframe = ttk.Frame(root.image_frame)
        subframe.pack(side="left", padx=10)

        imglabel_f = Label(subframe, image=img_f, background="#ddd")
        imglabel_f.pack()

        label = ttk.Label(subframe, text=f"T_f:")
        label.pack(pady=5)

        subframe = ttk.Frame(root.image_frame)
        subframe.pack(side="left", padx=10)

        imglabel_g = Label(subframe, image=img_g, background="#ddd")
        imglabel_g.pack()


        label = ttk.Label(subframe, text=f"T_g:")
        label.pack(pady=5)

        subframe = ttk.Frame(root.image_frame)
        subframe.pack(side="left", padx=10)

        imglabel_d = Label(subframe, image=img_d, background="#ddd")
        imglabel_d.pack()

        label = ttk.Label(subframe, text=f"Inferred Domain:")
        label.pack(pady=5)


        

root = Tk()
root.title("SI2DLA Visualization Tool")
root.resizable(False, False)

outer_frame = ttk.Frame(root, padding="40 40 40 40")
outer_frame.pack(fill="both", expand=True)

root.title_label = ttk.Label(outer_frame, text="SI2DLA Visualization Tool", font=("Calibri", 18, "bold"))
root.title_label.pack(pady=20)

root.execute_button = ttk.Button(outer_frame, text="Upload CSV", command=file_execute)
root.execute_button.pack()

       
root.image_frame = ttk.Frame(outer_frame)
root.image_frame.pack(pady=20)
root.image_frame.pack_forget()


# D_entry = scrolledtext.ScrolledText(mainframe, width=48, height=15)
# D_entry.grid(column=1, row=2, pady=16)

# R_label=Label(mainframe, text="insert input alphabet here (Rho):", anchor='sw', width=58)
# R_label.grid(column=1, row=3)

# R_entry = Text(mainframe, width=50, height=3)
# R_entry.grid(column=1, row=4, pady=16)

# S_label=Label(mainframe, text="insert output alphabet here (Sigma):", anchor='sw', width=58)
# S_label.grid(column=1, row=5)

# S_entry = Text(mainframe, width=50, height=3)
# S_entry.grid(column=1, row=6, pady=16)

# button = Button(mainframe, text="execute", command=file_execute)
# button.grid(column=1, row=9, pady=16)

# file_button = Button(mainframe, text="Upload CSV", command=file_execute)
# file_button.grid(column=3, row=1, pady=32)

root.mainloop()