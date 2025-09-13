from si2dla_new import *
# from si2dla_test import *
from ostia_d import ostia_d
from ostia import ostia
# from si2dla_robust import *
from k_tssi import *
from domain_inference import *
from helper import *
from data import assimilation, flap, chandleejardine, huajardine, kisd, opacity, sri_lanka_creole, yawelmani, zapotec, deletion


data = [
    (['root1'], ['t', 'a', 'd1']),
    (['root2'], ['t', 'a', 't']),
    (["root3"], ['t', 'a', 'd1', 'a']),
    (["root1", 'suff1'], ['t', 'a', 'd1', 'd1', 'a']),
    (["root2", 'suff1'], ['t', 'a', 't', 't', 'a']),
    (["root3", 'suff1'], ['t', 'a', 'd1', 'a', 't', 'a']),
    (["root1", 'suff2'], ['t', 'a', 'd1', 'd1', 'a']),
    (["root2", 'suff2'], ['t', 'a', 't','d1', 'a']),
    (["root3", 'suff2'], ['t', 'a', 'd1', 'a', 'd1', 'a']),
]

sigma = ['root1', 'root2', 'root3', 'suff1', 'suff2']
gamma = ['t', 'a', 'd1']



def run_test_list_format(d, r, s):

    si2dla_ex("", d, r, s)


def run_test(d, r, s):

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
    

# run_test(opacity.Data, opacity.Sigma, opacity.Gamma)
run_test_list_format(data, sigma, gamma)
