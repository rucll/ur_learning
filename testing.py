from si2dla import *
from experimental import * 

## ISL data

# Example 1 from Hua & Jardine 2021

D1 = [
    ("",""),
    ("w","aa"),
    ("x","cbcb"),
    ("y","bc"),
    ("z","bca"),
    ("ww","aaaa"),
    ("wx", "aacbcb"),
    ("wy", "aabc"),
    ("wz", "aabca"),
    ("xw", "cbcbaa"),
    ("xx", "cbcbcbcb"),
    ("xy", "cbcbbc"),
    ("xz", "cbcbbca"),
    ("yw", "bcaa"),
    ("yx", "bccbcb"),
    ("yy", "bcbc"),
    ("yz", "bcbca"),
    ("zw", "bcaaa"),
    ("zx", "bcacbcb"),
    ("zy", "bcaac"),
    ("zz", "bcaaca"),
]

R1 = ["w","x","y","z"]
S1 = ["a","b","c"]


# Assimilation
D2 = [
    ("1", "tat"),
    ("2", "a"),
    ("3", "tad"),
    ("4", "tadd"),
    ("A", "ta"),
    ("B", "da"),
    ("11", "tattat"),
    ("12", "tata"),
    ("13", "tattad"),
    ("14", "tattadd"),
    ("1A", "tatta"),
    ("1B", "tatda"),
    ("21", "atat"),
    ("22", "aa"),
    ("23", "atad"),
    ("24", "atadd"),
    ("2A", "ata"),
    ("2B", "ada"),
    ("31", "taddat"),
    ("32", "tada"),
    ("33", "taddad"),
    ("34", "taddadd"),
    ("3A", "tadda"),
    ("3B", "tadda"),
    ("41", "taddtat"),
    ("42", "tadda"),
    ("43", "taddtad"),
    ("44", "taddtadd"),
    ("4A", "taddta"),
    ("4B", "taddda"),
    ("A1", "tatat"),
    ("A2", "taa"),
    ("A3", "tatad"),
    ("A4", "tatadd"),
    ("AA", "tata"),
    ("AB", "tada"),
    ("B1", "datat"),
    ("B2", "daa"),
    ("B3", "datad"),
    ("B4", "datadd"),
    ("BA", "data"),
    ("BB", "dada"),
    ("333", "taddaddad"), #This appears necessary to get 3 to go to state 3 instead of state ''
    ("444", "taddtaddtadd"),
]


R2 = ["1","2","3","4","A","B"]
S2 = ["a","d","t"]


# Deletion (t -> 0 / t _ )
D3 = [
    ("1", "tat"),
    ("2", "a"),
    ("3", "tad"),
    ("A", "ta"),
    ("B", "da"),
    ("11", "tatat"),
    ("12", "tata"),
    ("13", "tatad"),
    ("1A", "tata"),
    ("1B", "tatda"),
    ("21", "atat"),
    ("22", "aa"),
    ("23", "atad"),
    ("2A", "ata"),
    ("2B", "ada"),
    ("31", "tadtat"),
    ("32", "tada"),
    ("33", "tadtad"),
    ("3A", "tadta"),
    ("3B", "tadda"),
    ("A1", "tatat"),
    ("A2", "taa"),
    ("A3", "tatad"),
    ("AA", "tata"),
    ("AB", "tada"),
    ("B1", "datat"),
    ("B2", "daa"),
    ("B3", "datad"),
    ("BA", "data"),
    ("BB", "dada"),
]



# Assimilation with less data
D4 = [
    ("1", "tat"),
    ("2", "a"),
    ("3", "tad"),
    ("4", "tadd"),
    ("A", "ta"),
    ("B", "da"),
    ("3A", "tadda"),
    ("3B", "tadda"),
    # ("11", "tattat"),
    # ("12", "tata"),
    # ("13", "tattad"),
    # ("14", "tattadd"),
    ("1A", "tatta"),
    ("1B", "tatda"),
    # ("21", "atat"),
    # ("22", "aa"),
    # ("23", "atad"),
    # ("24", "atadd"),
    # ("2A", "ata"),
    # ("2B", "ada"),
    # ("31", "taddat"),
    # ("32", "tada"),
    # ("33", "taddad"),
    # ("34", "taddadd"),
    # ("3A", "tadda"),
    # ("3B", "tadda"),
    # ("41", "taddtat"),
    # ("42", "tadda"),
    # ("43", "taddtad"),
    # ("44", "taddtadd"),
    # ("4A", "taddta"),
    # ("4B", "taddda"),
    # ("A1", "tatat"),
    # ("A2", "taa"),
    # ("A3", "tatad"),
    # ("A4", "tatadd"),
    # ("AA", "tata"),
    # ("AB", "tada"),
    # ("B1", "datat"),
    # ("B2", "daa"),
    # ("B3", "datad"),
    # ("B4", "datadd"),
    # ("BA", "data"),
    # ("BB", "dada"),
]


## OSL data

# Assimilation
D5 = [
    ("1", "tat"),
    ("2", "a"),
    ("3", "tad"),
    ("A", "ta"),
    ("B", "da"),
    ("11", "tattat"),
    ("12", "tata"),
    ("13", "tattad"),
    ("1A", "tatta"),
    ("1B", "tatda"),
    ("21", "atat"),
    ("22", "aa"),
    ("23", "atad"),
    ("2A", "ata"),
    ("2B", "ada"),
    ("31", "taddat"),
    ("32", "tada"),
    ("33", "taddad"),
    ("3A", "tadda"),
    ("3B", "tadda"),
    ("A1", "tatat"),
    ("A2", "taa"),
    ("A3", "tatad"),
    ("AA", "tata"),
    ("AB", "tada"),
    ("B1", "datat"),
    ("B2", "daa"),
    ("B3", "datad"),
    ("BA", "data"),
    ("BB", "dada"),
    ("333", "taddaddad"), #This appears necessary to get 3 to go to state 3 instead of state ''
]

iT_f, iT_g = si2dla_ex(D2,R2,S2)
oT_f, oT_g = so2dla_ex(D5,R2,S2)
