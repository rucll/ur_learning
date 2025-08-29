from si2dla_new import *
# from si2dla_test import *
from ostia_d import ostia_d
# from si2dla import *
from k_tssi import *
from domain_inference import *
from helper import *
from data import assimilation, flap, chandleejardine, huajardine, kisd, opacity, sri_lanka_creole, yawelmani, zapotec, deletion


def run_test(d, r, s):

    T = infer_domain(d)

    # if there are 2 states in domain inference, then the domain is Sigma star
    if len(T.Q) == 2:
        sigma_star = []

        for tr in T.E:
            if tr[0] != 0:
                sigma_star.append(tr)

        T.E = sigma_star
        T.Q.remove(0)


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


run_test(zapotec.Data, zapotec.Sigma, zapotec.Gamma)
