from si2dla_new import *
# from si2dla_test import *
from ostia_d import ostia_d
from ostia import ostia
# from si2dla import *
from k_tssi import *
from domain_inference import *
from helper import *
from data import flap, chandleejardine, huajardine, kisd, opacity, sri_lanka_creole, yawelmani, zapotec


Data = [
    (["1"], ["t", "a", "d"]),
    (["2"], ["t", "a", "t"]),
    (["3"], ["t", "a", "d", "a"]),
    (["1","Az"], ["t", "a", "d", "d", "a"]),
    (["2", "Az"], ["t", "a", "t", "t", "a"]),
    (["3", "Az"], ["t", "a", "d", "a", "t", "a"]),
    (["1", "B"], ["t", "a", "d", "d", "a"]),
    (["2", "B"], ["t", "a", "t", "d", "a"]),
    (["3", "B"], ["t", "a", "d", "a", "d", "a"])]
Sigma = ["1", "2", "3", "Az", "B"]
Gamma = ["t", "a", "d"]
# Data = [
#     ("1", "tad"),
#     ("2", "tat"),
#     ("3", "tada"),
#     ("1A", "tadda"),
#     ("2A", "tatta"),
#     ("3A", "tadata"),
#     ("1B", "tadda"),
#     ("2B", "tatda"),
#     ("3B", "tadada")
#     ]
# Sigma = ["1", "2", "3", "A", "B"]
# Gamma = ["t", "a", "d"]

ostia(Data, Sigma, Gamma)


# def run_test(d, r, s):

#     T = infer_domain(d)

#     print("Domain: ", T.E)

#     T_f = ostia_d(T, d, r, s)

#     print(T_f.E)

#     print("OSTIA: ", T_f.E)
#     T_f, T_g = si2dla_ex(T, d, r, s)
#     print(f"Phonology: {T_g.E}")
#     for i, o in d:
#         print(f"{i} => {o}")
#         assert(T_g.rewrite(T_f.rewrite(i)) == o)

#     print("All checks passed!")


# run_test(Data, Sigma, Gamma)