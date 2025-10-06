"""
Written by Ezra Anthony 

last edited by Ezra Anthony September 2025

Reads the CSV input, and outputs a list of tuples of lists, where the tuples tie sounds to meanings

"""

import csv

#make a list of tuples called data:
data = []

with open('data/Yagba_Nasalharmony.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        
        row1 = str(row[0])
        row2 = str(row[1])

        d1 = []
        d2 = []
        
        #removing unnecessary chars
        row2 = row2.replace(' [', "")
        row2 = row2.replace(']', "")

        
        d1.extend(row1.split(" "))
        d1.remove('')
        d2.extend(row2.split("; "))

        
        #making a tuple of the lists d1 and d2, and adding that tuple to the list data
        tuple_of_lists = tuple([d1, d2])
        
        data.append(tuple_of_lists)

    print(data)

