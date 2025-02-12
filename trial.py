from si2dla_mod import *

# rub - A
# cast - B
# face - C
# get up and go early - D
# reach a destination - E
# fly - F
# uncover - G
# flow - H

# perfective - 2

D1 = [
    ("2","ia"),
    ("22","iaia"),
    ("A","olo"),
    ("B","lafo"),
    ("C","ana"),
    ("D","usu"),
    ("E","tau"),
    ("F", "lele"),
    ("G", "su?e"),
    ("H", "tafe"),
    ("A2","oloia"),
    ("B2","lafoia"),
    ("C2","anaia"),
    ("D2","usuia"),
    ("E2","tauia"),
    ("F2", "lelea"),
    ("G2", "su?ea"),
    ("H2", "tafea"),
    ("AA","oloolo"),
    ("AB","ololafo"),
    ("AC","oloana"),
    ("AD","olousu"),
    ("AE","olotau"),
    ("AF", "ololele"),
    ("AG", "olosu?e"),
    ("AH", "olotafe"),
    ("AA2","olooloia"),
    ("BB2","lafolafoia"),
    ("CC2","anaanaia"),
    ("DD2","usuusuia"),
    ("EE2","tautauia"),
    ("FF2", "lelelelea"),
    ("GG2", "su?esu?ea"),
    ("HH2", "tafetafea"),
    ("AB","ololafo"),
    ("BC","lafoana"),
    ("CD","anausu"),
    ("DE","usutau"),
    ("EF","taulele"),
    ("FG", "lelesu?e"),
    ("GH", "su?etafe"),
    ("FA","leleolo"),
    ("FB","lelelafo"),
    ("FC","leleana"),
    ("FD","leleusu"),
    ("FE","leletau"),
    ("FF","lelelele"),
    ("FG", "lelesu?e"),
    ("FH", "leletafe"),
    ("HA", "tafeolo"),
    ("BA","lafoolo"),
    ("CB","analafo"),
    ("DC","usuana"),
    ("ED","tauusu"),
    ("FE","leletau"),
    ("GF", "su?elele"),
    ("HG", "tafesu?e"),
    ("AH", "olotafe"),
    ("AB2","ololafoia"),
    ("BC2","lafoanaia"),
    ("CD2","anausuia"),
    ("DE2","usutauia"),
    ("EF2","taulelea"),
    ("FG2", "lelesu?ea"),
    ("GH2", "su?etafea"),
    ("FA2","leleoloia"),
    ("FB2","lelelafoia"),
    ("FC2","leleanaia"),
    ("FD2","leleusuia"),
    ("FE2","leletauia"),
    ("FG2", "lelesu?ea"),
    ("FH2", "leletafea"),
    ("HA2", "tafeoloia"),
    ("BA2","lafooloia"),
    ("CB2","analafoia"),
    ("DC2","usuanaia"),
    ("ED2","tauusuia"),
    ("FE2","leletauia"),
    ("GF2", "su?elelea"),
    ("HG2", "tafesu?ea"),
    ("AH2", "olotafea"),
    ("2AA","iaoloolo"),
    ("2BB","ialafolafo"),
    ("2CC","iaanaana"),
    ("2DD","iausuusu"),
    ("2EE","iatautau"),
    ("2FF", "ialelelele"),
    ("2GG", "iasu?esu?e"),
    ("2HH", "iatafetafe"),
    ("ABA","ololafoolo"),
    ("BCB","lafoanalafo"),
    ("CDC","anausuana"),
    ("DED","usutauusu"),
    ("EFE","tauleletau"),
    ("FGF", "lelesu?elele"),
    ("GHG", "su?etafesu?e"),
    ("HAH", "tafeolotafe"),
]


R1 = ["A", "B", "C", "D", "E", "F", "G", "H", "2"]
S1 = ["o", "l", "a", "f", "n", "u", "s", "t", "e", "?", "i"]

# D1 = [
#     ("",""),
#     ("A1","olo"),
#     ("B1","lafo"),
#     ("C1","ana"),
#     ("D1","usu"),
#     ("E1","tau"),
#     ("F1", "lele"),
#     ("G1", "su?e"),
#     ("H1", "tafe"),
#     ("A2","oloia"),
#     ("B2","lafoia"),
#     ("C2","anaia"),
#     ("D2","usuia"),
#     ("E2","tauia"),
#     ("F2", "lelea"),
#     ("G2", "su?ea"),
#     ("H2", "tafea"),
# ]

T_f, T_g = si2dla(D1,R1,S1)