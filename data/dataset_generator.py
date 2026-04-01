'''
Dataset Generator
created by Ezra Anthony 3/2026
last by EA edited 3/2026


Notes:
Take in info about what change is (input, output)
(Way to take care of deletion-- e.g. 'x' --> '')
Morphemes as dict
Right hand context and left hand context – if not one then it should be None, if word boundary then '#'
Hashes in input, don’t need word boundaries for morpheme string
return array of tuples


Note 3/30/2026 doesn't work if right context = '#'
'''


import csv
import tkinter as tk
from tkinter import messagebox
import ast

def dataset_generator(left_context, right_context, morphemes, input, output):
    dataset = []
    for tuple1 in morphemes:
        dataset.append(tuple1)
        for tuple2 in morphemes:
            dataset.append(tuple([(tuple1[0] + " " + tuple2[0]), str(tuple1[1] + " " + tuple2[1])]))
            if right_context != None and left_context != None:
                for tuple3 in morphemes:
                    dataset.append(tuple([(tuple1[0] + " " + tuple2[0] + " " + tuple3[0]), (tuple1[1] + " " + tuple2[1] + ' ' + tuple3[1])]))
   

    for i in range(len(dataset)):
        #data[1].replace(find_string, replace_string)
        replacement_value = dataset[i][1]
        if(right_context == '#'):
            '''if dataset[i][1][:-(len(left_context + " " + input))] == (left_context + " " + input):
                replacement_value = dataset[i][1][:-(len(input))] + output
            '''
            if (left_context == None):
                if (dataset[i][1].find(input) == (len(dataset[i][1]) - len(input) -1)):
                    replacement_value = dataset[i][1][:-(len(input))] + output


            elif (dataset[i][1].find(left_context + " " + input) == (len(dataset[i][1]) - len(left_context + " " + input) - 1)):
                replacement_value = dataset[i][1][:-(len(input))] + output


        elif(left_context == '#'):
            if (right_context == None):
                if (dataset[i][1].find(input) == 0):
                    replacement_value = output + dataset[i][1][1:]
            elif (dataset[i][1].find(input + " " + right_context) == 0):
                replacement_value = output + dataset[i][1][1:]


        else:
            if (right_context == None):
                find_string = str(left_context + " " + input)
                replace_string = str(left_context + " " + output)
           
            elif (left_context == None):
                find_string = str(input + " " + right_context)
                replace_string = str(output + " " + right_context)


            else:
                find_string = str(left_context + " " + input + " " + right_context)
                replace_string = str(left_context + " " + output + " " + right_context)
               
            replacement_value = str(dataset[i][1]).replace(find_string, replace_string)


        #split by spaces, make into tuple inside the tuple
        split_value = tuple(replacement_value.split())
        split_key = tuple(str(dataset[i][0]).split())
        dataset[i] = tuple([split_key, split_value])


    return dataset




import csv


def write_to_csv(filename, dataset):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
       
        for letters, chars in dataset:
            # join characters with spaces
            left = " ".join(chars)


            # join letters with semicolons inside brackets
            right = " ".join(letters)


            writer.writerow([left , right])




my_morphemes = [('A', 't a t'), ('B', 't a d t'), ('C', 'a'), ('D', 't a d'), ('E', 't')]
#print(dataset_generator('a', 'a', my_morphemes, 't', 'd'))


#write_to_csv("test3.csv", dataset_generator('a', 'a', my_morphemes, 't', 'd'))
write_to_csv("test3.csv", dataset_generator('a', 'a', my_morphemes, 't', 'd'))
'''
print(dataset_generator('#', 'a', my_morphemes, 't', 'd'))
'''
'''
print()


print(dataset_generator('a', '#', my_morphemes, 't', 'd'))
'''

def parse_morphemes(text):
    """
    supports two formats:

    1. line format:
       A:t a t
       B:t a d t

    2. python list format:
       [('A', 't a t'), ('B', 't a d t')] etc.
    """

    text = text.strip()

    try:
        parsed = ast.literal_eval(text)

        if isinstance(parsed, list):
            morphemes = []
            for item in parsed:
                if isinstance(item, tuple) and len(item) == 2:
                    key, value = item
                    morphemes.append((str(key), str(value)))
            if morphemes:
                return morphemes
    except:
        pass  # fall back to manual parsing if you can't parse as python list

    morphemes = []
    lines = text.split("\n")
    for line in lines:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        morphemes.append((key.strip(), value.strip()))

    return morphemes


def generate_dataset():
    try:
        morphemes_text = morphemes_input.get("1.0", tk.END)
        morphemes = parse_morphemes(morphemes_text)

        left = left_context_entry.get().strip()
        right = right_context_entry.get().strip()
        inp = input_entry.get().strip()
        out = output_entry.get().strip()
        filename = filename_entry.get().strip()

        left = None if left == "" else left
        right = None if right == "" else right

        dataset = dataset_generator(left, right, morphemes, inp, out)
        write_to_csv(filename, dataset)

        messagebox.showinfo("Success", f"Dataset written to {filename}!")

    except Exception as e:
        messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title("Dataset Generator")

tk.Label(root, text="Morphemes (format: A:t a t or Python list format)").pack()
morphemes_input = tk.Text(root, height=8, width=50)
morphemes_input.pack()

tk.Label(root, text="Left Context").pack()
left_context_entry = tk.Entry(root)
left_context_entry.pack()

tk.Label(root, text="Right Context").pack()
right_context_entry = tk.Entry(root)
right_context_entry.pack()

tk.Label(root, text="Target Symbol (input)").pack()
input_entry = tk.Entry(root)
input_entry.pack()

tk.Label(root, text="Output Symbol").pack()
output_entry = tk.Entry(root)
output_entry.pack()

tk.Label(root, text="Output CSV Filename").pack()
filename_entry = tk.Entry(root)
filename_entry.insert(0, "output.csv")
filename_entry.pack()

# Generate button
tk.Button(root, text="Generate Dataset", command=generate_dataset).pack(pady=10)

root.mainloop()