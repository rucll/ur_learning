from si2dla import *

# Example 1 from Hua & Jardine 2021

D = [
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

T_f, T_g = si2dla(D,["w","x","y","z"],["a","b","c"])


# Assimilation
D = [
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
]


T_f, T_g = si2dla(D,["1","2","3","4","A","B"],["a","d","t"])
