import sys
sys.path.append('..')
from si2dla_new import *
# from si2dla_test import *
from ostia_d import ostia_d
from k_tssi import *
from domain_inference import *
from helper import *
from parser import parse_csv


def read_alphabet(D_list):   
    R_list = []
    S_list = []
    for data_pair in D_list:
        R_list.extend(data_pair[0])
        S_list.extend(data_pair[1])

    R_list = list(set(R_list))
    S_list = list(set(S_list))
    return (R_list, S_list)

def run_test(data_csv):

    d = parse_csv(data_csv)

    print(d)

    (r, s) = read_alphabet(d)


    T = infer_domain(d)

    print("Domain: ", T.E)

    T_f = ostia_d(T, d, r, s)

    print(T_f.E)

    print("OSTIA: ", T_f.E)
    T_f, T_g = si2dla_ex(T, d, r, s)
    print(f"Phonology: {T_g.E}")
    for i, o in d:
        print(f"{i} => {o}")
        assert(T_g.rewrite(T_f.rewrite(i)) == o)

    print("All checks passed!")

run_test('data/demo_data/chandleejardine.csv')
