"""A class defining a Featural Finite State Transducer, based on FST by Alena Aksenova.

  This is just for testing and not verifiably correct in any way.

  by Adam Jardine
"""

from copy import deepcopy


def invert(F):
    """Return a dictionary R that maps feature sets in F to symbols"""
    R = {}
    for f, S in F.items():
        R[S] = f
    return R


def rep_feat(a,S,T,F):
    """Return set by replacing subset S of features of a with T"""
    return (F[a]-S).union(T)


class FFST:
    """A class representing featural finite state transducers.

    Attributes:
        Q (list): a list of states;
        Phi (set): a set of feature symbols
        qe (str): name of the unique initial state;
        E (list): a list of transitions;
        stout (dict): a collection of state outputs.
    """

    def __init__(self,Phi=None):
        """Initializes the FFST object."""
        self.Q = None
        self.Phi = Phi
        self.qe = ""
        self.E = None   # Tuple of the form (state,tuple,tuple,state)
        self.stout = None

    def rewrite(self, w, F):
        """Rewrites the given string with respect to the rules represented in
        the current FFST.

        Arguments:
            w (str): a string that needs to be rewritten.
            F: a feature mapping from symbols in w to sets of features (must be subsets of Phi)
        Outputs:
            str: the translation of the input string.
        """
        if self.Q == None:
            raise ValueError("The transducer needs to be constructed.")

        # move through the transducer and write the output
        result = ""
        current_state = self.qe
        moved = False
        for i in range(len(w)):
            for tr in self.E:
                if tr[0] == current_state and tr[1].issubset(F[w[i]]):
                    outset = rep_feat(w[i],tr[1],tr[2],F)
                    if outset in invert(F):
                        result += invert(F)[outset]
                    else:
                        raise ValueError(
                            "Transducer creates set {s} not mapped in feature dictionary provided".format(s=outset)
                        )
                    current_state, moved = tr[3], True
                    break
            if moved == False:
                raise ValueError(
                    "This string cannot be read by the current transducer (didn't have transition on {q},{S}).".format(q=current_state,S=F[w[i]])
                )

        # add the final state output
        if self.stout[current_state] != "*":
            if self.stout[current_state] == set([]):
                result += ""
            elif self.stout[current_state] in invert(F):
                result += invert(F)[self.stout[current_state]]
            else:
                raise ValueError(
                    "Transducer creates set {s} not mapped in feature dictionary provided".format(s=str(self.stout[current_state]))
                )

        return result

    def copy_fst(self):
        """Produces a deep copy of the current FFST.

        Returns:
            T (FFST): a copy of the current FFST.
        """
        T = FST()
        T.Q = deepcopy(self.Q)
        T.Phi = deepcopy(self.Phi)
        T.E = deepcopy(self.E)
        T.stout = deepcopy(self.stout)

        return T
