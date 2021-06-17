from fst_object import *
from ostia import *
from helper import *


# Helper functions

def suff_1(w):
    """Returns 1-suffix of w"""
    if w == "":
        return ""
    else:
        return w[-1]


def get_OS(T,q):
    """Gets output 1-suffixes of state q in FST T"""
    incoming = { tr for tr in T.E if tr[3] == q}
    outs = { tr[2] for tr in incoming}
    suffs = { suff_1(w) for w in outs}
    return suffs


def lncat(w,v):
    """Returns wv^-1; i.e. v removed from the end of w"""
    if w.endswith(v):
        return w[0:-len(v)]


# Main algorithm

def si2dla(D,Rho,Sigma):
    """Implements SI2LDA from Hua & Jardine 2021"""

    T_f = ostia(D,Rho,Sigma)

    print("Initial hypothesis for T_f:")
    print("  Q:\t"+str(T_f.Q))
    print("  E:\t"+str(T_f.E))
    print("  q0:\t"+str(T_f.qe))
    print("  stout:\t"+str(T_f.stout))

    q1 = T_f.Q[0]
    q2 = T_f.Q[1]

    OS = { q1 : get_OS(T_f,q1) | {""},
           q2 : get_OS(T_f,q2)
    }

    print("OSs for T_f:\t"+str(OS))

    #*** construct T_g

    Q_g = ["qe","qd"]

    corr = {}
    rroc = {}

    if len(OS[q1]) < len(OS[q2]):
        corr["qe"] = q1
        corr["qd"] = q2
        rroc[q1] = "qe"
        rroc[q2] = "qd"
    else:
        corr["qe"] = q2
        corr["qd"] = q1
        rroc[q2] = "qe"
        rroc[q1] = "qd"

    print("corr:\t\t"+str(corr))
    # print("rroc:\t\t"+str(rroc))

    IS = { "qe" : OS[corr["qe"]],
           "qd" : OS[corr["qd"]]
    }

    if len(IS["qe"]) > 1:
        IS["qe"] = IS["qe"] - (IS["qe"] & IS["qd"])
    IS["qd"] = IS["qd"] - (IS["qe"] & IS["qd"])

    print("ISs for T_g:\t"+str(IS))


    d_g = {}

    for q in Q_g:
        for s in Sigma:
            for r in Q_g:
                if s in IS[r]:
                    d_g[(q,s)] = r

    print("d_g:\t"+str(d_g))

    o_g = {}

    for s in Sigma:
        o_g[("q_d",s)] = s

        d_tr = [ tr for tr in T_f.E if tr[0] == corr["qd"] and tr[2][0] == s ][0]

        w_d = d_tr[2]

        w_e = [ tr[2] for tr in T_f.E if tr[0] == corr["qe"] and tr[1] == d_tr[1]][0]

        o_g[("q_e",s)] = lncat(w_e,w_d[1:])

        # print(w_d," ",w_e)

    print("o_g:\t"+str(o_g))


    T_g = FST(Rho,Sigma)

    return (T_f,T_g)
