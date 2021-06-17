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

    # construct T_g
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

    # return OS
