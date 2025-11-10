"""A featural version of the SI2DLA of Hua & Jardine (2021).

  This is for testing only and not verifiably correct in any way.

  Written by Adam Jardine.
"""

from utility.fst_object import *
from ostia import *
from utility.helper import *
from features import *


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
    if v == "":
        return w
    elif w.endswith(v):
        return w[0:-len(v)]


# Main algorithm

def fsi2dla(D,Rho,Sigma):
    """Implements the FSI2LDA"""

    # To do!
