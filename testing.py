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

si2dla(D,["w","x","y","z"],["a","b","c"])
