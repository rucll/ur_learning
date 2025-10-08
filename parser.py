"""
Written by Ezra Anthony 

last edited by Ezra Anthony September 2025

Reads the CSV input, and outputs a list of tuples of lists, where the tuples tie sounds to meanings

"""

import csv

def parse_csv(filepath):
        
    #make a list of tuples called data:
    data = []

    with open(filepath, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:

            print(row)
            row1 = str(row[0])
            row2 = str(row[1])

            d1 = []
            d2 = []
            
            #removing unnecessary chars
            row2 = row2.replace(' [', "")
            row2 = row2.replace(']', "")

            
            d1.extend(row1.split(" "))
            # d1.remove('')
            d2.extend(row2.split("; "))

            tup_d1 = tuple(d1)
            tup_d2 = tuple(d2)
            #making a tuple of the lists d1 and d2, and adding that tuple to the list data
            tuple_of_tuples = tuple([tup_d1, tup_d2])
            
            data.append(tuple_of_tuples)

        # print(data)
        return(data)

parse_csv("data/nagoya_japanese_haraguchi_2.1.csv")