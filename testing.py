from si2dla import *
from so2dla import *
from fsi2dla import *
from idla import *
from data import flap, yawelmani, huajardine, zapotec, opacity

## ISL data



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

# iT_f, iT_g = si2dla_ex(D2,R2,S2)
# oT_f, oT_g = so2dla_ex(D5,R2,S2)


## For testing FSI2DLA

S3 = ["t","k","a","d","g"]
F3 = { 't': frozenset({"-s","-v","-b"}),
       'd': frozenset({"-s","+v","-b"}),
       'a': frozenset({"+s","+b"}),
       'k': frozenset({"-s","-v","+b"}),
       'g': frozenset({"-s","+v","+b"}),
       '': frozenset({"#"}),
}

T3 = FFST()
T3.Q = ["0","1"]
T3.qe = "0"
T3.E = [("0",{"-v"},{"-v"},"0"),
        ("0",{"+s"},{"+s"},"0"),
        ("0",{"-s","+v"},{"-s","+v"},"1"),
        ("1",{"-v"},{"+v"},"0"),
        ("1",{"+s","+v"},{"+s","+v"},"0"),
        ("1",{"-s","+v"},{"-s","+v"},"1"),
        ]
T3.stout = {"0":set([]),"1":set([])}

D6 = [
    ("1", "tat"),
    ("2", "a"),
    ("3", "tad"),
    ("4", "tag"),
    ("A", "ta"),
    ("B", "da"),
    ("C", "ka"),
    ("11", "tattat"),
    ("12", "tata"),
    ("13", "tattad"),
    ("14", "tattag"),
    ("1A", "tatta"),
    ("1B", "tatda"),
    ("1C", "tatka"),
    ("21", "atat"),
    ("22", "aa"),
    ("23", "atad"),
    ("24", "atag"),
    ("2A", "ata"),
    ("2B", "ada"),
    ("2C", "aka"),
    ("31", "taddat"),
    ("32", "tada"),
    ("33", "taddad"),
    ("34", "taddag"),
    ("3A", "tadda"),
    ("3B", "tadda"),
    ("3C", "tadga"),
    ("41", "tagdat"),
    ("42", "taga"),
    ("43", "tagdad"),
    ("44", "tagdag"),
    ("4A", "tagda"),
    ("4B", "tagda"),
    ("4C", "tagga"),
    ("A1", "tatat"),
    ("A2", "taa"),
    ("A3", "tatad"),
    ("A4", "tatag"),
    ("AA", "tata"),
    ("AB", "tada"),
    ("AC", "taka"),
    ("B1", "datat"),
    ("B2", "daa"),
    ("B3", "datad"),
    ("B4", "datag"),
    ("BA", "data"),
    ("BB", "dada"),
    ("BC", "daka"),
    ("C1", "katat"),
    ("C2", "kaa"),
    ("C3", "katad"),
    ("C4", "katag"),
    ("CA", "kata"),
    ("CB", "kada"),
    ("CC", "kaka"),
]

# FT_f, FT_g = fsi2dla(D6,R2,S3,F3)
#T_f, T_g = si2dla(D1,R1,S1)
def print_edge(E, name):
	print("="*12, name, "="*12);
	for e in E:
		print(f"\t{e}");

for x in [yawelmani, flap, huajardine, opacity]:
	f, g = idla(x.Data, x.Sigma, x.Gamma);
	print_edge(f.E, "f");
	print_edge(g.E, "g");

	for i, o in x.Data:
		print(f"checking: {i} -> {o}");
		assert(g.rewrite(f.rewrite(i)) == o);
	print("All checks passed!");
