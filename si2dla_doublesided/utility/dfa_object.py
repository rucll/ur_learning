from copy import deepcopy

class DFA:
    """A class representing finite state transducers.

    Attributes:
        Q (list): a list of states;
        Sigma (list): a list of symbols of the input alphabet;
        Gamma (list): a list of symbols of the output alphabet;
        qe (str): name of the unique initial state;
        qf (list): a list of final states
        E (list): a list of transitions;
        stout (dict): a collection of state outputs.
    """

    def __init__(self, Sigma=None, Gamma=None):
        """Initializes the DFA object."""
        self.Q = None
        self.Sigma = Sigma
        self.Gamma = Gamma
        self.qe = ""
        self.qf = None
        self.E = None
        self.stout = None

    def rewrite(self, w):
        """Rewrites the given string with respect to the rules represented in
        the current DFA.

        Arguments:
            w (str): a string that needs to be rewritten.
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
                if tr[0] == current_state and tr[1] == w[i]:
                    result += tr[2]
                    current_state, moved = tr[3], True
                    break
            if moved == False:
                raise ValueError(
                    "This string cannot be read by the current transducer."
                )

        # add the final state output
        if self.stout[current_state] != "*":
            result += self.stout[current_state]

        return result

    def copy_DFA(self):
        """Produces a deep copy of the current DFA.

        Returns:
            T (DFA): a copy of the current DFA.
        """
        T = DFA()
        T.Q = deepcopy(self.Q)
        T.qf = deepcopy(self.qf)
        T.Sigma = deepcopy(self.Sigma)
        T.Gamma = deepcopy(self.Gamma)
        T.E = deepcopy(self.E)
        T.stout = deepcopy(self.stout)

        return T
