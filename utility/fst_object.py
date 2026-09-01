"""A class defining the Finite State Transducer.
Copyright (C) 2019 Alena Aksenova.
Copyright (C) 2026 William Schilling.

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 3 of the License, or (at your
option) any later version.

Modified by William (Liam) Schilling:

Implemented core finite-state operations,
taking `FST` to be a general (potentially nondeterministic) finite-state transducer
that accepts a relation over strings.
Added trimming, inversion, concatenation, Kleene closure, union, composition, and determinization.

Exposed additional variations of rewrite and transition functions to the user.
The previous implementation of `rewrite` has been divided into some smaller functions,
but the resulting `rewrite` function has the same behavior as before.

These functions assume the following `FST` representation invariants, stated as type annotations:
    Q (Annotated[list[str], "no duplicates"])
    Sigma (Annotated[list[Annotated[str, "length==1"]], "no duplicates"])
    Gamma (Annotated[list[Annotated[str, "length==1"]], "no duplicates"])
    qe (Annotated[str, "in Q"])
    E (Annotated[list[
            Annotated[str, "in Q"],
            Annotated[str, "alphabet is Sigma"],
            Annotated[str, "alphabet is Gamma"],
            Annotated[str, "in Q"]
        ], "no duplicates"])
    stout (dict[
            Annotated[str, "in Q"],
            Annotated[str, "alphabet is Gamma"]
        ])
As an additional note, we take states that are not keys of `stout` to be the rejecting states.
This is different from the `DFA` class in `dfa_object.py`, which marks accepting states separately.

The functions explicitly track the following useful FST properties.
The docstrings declare which are ensured by and which are invariants of the implementations.
- Trimmedness: Every state and transition is traversed by some accepting run
  (except in the edge case of the empty FST, which may only have one state and no transitions).
  Because of this edge case, some functions must take special care to be trimmedness-preserving.
- Final-output emptiness: Every final output (values of `stout`) is the empty string.
- Input-string expansion: The input string of every transition is either a character or empty.
- Determinism: The input string of every transition is a character,
  and for each state, every character is the input string of no more than one outgoing transition.
"""

from copy import deepcopy
from queue import Queue
from .helper import lcp

class FST:
    """A class representing finite state transducers.

    Attributes:
        name (str): a descriptive name for this FST.
        Q (list): a list of states.
        Sigma (list): a list of symbols of the input alphabet.
        Gamma (list): a list of symbols of the output alphabet.
        qe (str): name of the unique initial state.
        E (list): a list of transitions.
        stout (dict): a collection of state outputs.
    """

    def __init__(self, Sigma=None, Gamma=None):
        """Initializes the FST object."""
        self.name = "unnamed-FST"
        self.Q = None
        self.Sigma = Sigma
        self.Gamma = Gamma
        self.qe = ""
        self.E = None
        self.stout = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'''FST(
    name='{self.name}',
    (Sigma, Gamma)=({self.Sigma}, {self.Gamma}),
    Q={self.Q},
    qe='{self.qe}',
    E={self.E},
    stout={self.stout}
)'''

    def rewrite_from(self, q, w):
        """Performs a partial rewrite of the given string with respect to the rules represented in
        the current FST. That is, a rewrite starting from some intermediate state `q`.

        Arguments:
            q: the start state.
            w (str): a string that needs to be rewritten.

        Outputs:
            str: the translation of the input string starting from `q`.
        """
        if self.Q == None:
            raise ValueError("The transducer needs to be constructed.")

        # move through the transducer and write the output
        result = []
        current_state = q
        moved = False
        for i in range(len(w)):
            for tr in self.E:
                if tr[0] == current_state and tr[1] == w[i]:
                    if type(tr[2]) is str:
                        result.append(tr[2])
                    else:
                        result.extend(tr[2])
                    current_state, moved = tr[3], True
                    break
            if moved == False:
                raise ValueError(
                    "This string cannot be read by the current transducer."
                )

        # add the final state output
        if self.stout[current_state] != "*":
            result += self.stout[current_state]

        result = tuple(result)
        return result
    
    def rewrite(self, w):
        """Rewrites the given string with respect to the rules represented in
        the current FST.

        Arguments:
            w (str): a string that needs to be rewritten.

        Outputs:
            str: the translation of the input string.
        """
        return self.rewrite_from(self.qe, w)
    
    def flat_rewrite_from(self, q, w):
        """A version of `rewrite_from` that flattens the list of output strings into one string."""
        return "".join(self.rewrite_from(q, w))
    
    def flat_rewrite(self, w):
        """A version of `rewrite` that flattens the list of output strings into one string."""
        return "".join(self.rewrite(w))
    
    def transition_from(self, q, w):
        """Traverses from the state `q` according to the string `w`,
        and returns the resulting state.
        Returns `None` if a missing transition is encountered.

        Args:
            q: the start state.
            w (str): a string to read.

        Returns:
            the state reached by `w` from `q`, or `None`.
        """
        for c in w:
            moved = False
            for tr in self.E:
                if tr[0] == q and tr[1] == c:
                    q = tr[3]
                    moved = True
                    break
            if not moved:
                return None
        return q

    def in_domain_from(self, q, w):
        """Traverses from the state `q` according to the string `w`,
        and returns `True` iff the traversal is a success.

        Args:
            q: the start state.
            w (str): a string to read.

        Returns:
            `True` iff `w` is in the domain of the FST starting from `q`.
        """
        return self.transition_from(q, w) is not None

    def copy_fst(self):
        """Produces a deep copy of the current FST.

        Returns:
            T (FST): a copy of the current FST.
        """
        T = FST()
        T.name = deepcopy(self.name)
        T.Q = deepcopy(self.Q)
        T.Sigma = deepcopy(self.Sigma)
        T.Gamma = deepcopy(self.Gamma)
        T.qe = deepcopy(self.qe)
        T.E = deepcopy(self.E)
        T.stout = deepcopy(self.stout)
        return T

    def fresh_state(self, name_prefix):
        """Finds a name that is not the name of a state already in the FST.
        Specifically, returns the first available name of the form `f"{name_prefix}.{i}"`
        where `i` is a nonnegative integer.

        Args:
            name_prefix (str): guaranteed to be a prefix of the return value.
        
        Returns:
            str: a name that is guaranteed not to be the name of a state in the FST.
        """
        i = 0
        while True:
            name = f"{name_prefix}.{i}"
            if name not in self.Q:
                return name
            i += 1

    @staticmethod
    def encode_state(*args):
        """Returns a name that encodes the values of all the passed arguments.
        The encoding is guaranteed to be one-to-one as long as
        the string representations of the arguments do not contain `;`, `<`, or `>`,
        except for from previous invocations of this function.

        It is important that the client adhere to this condition in their FSTs,
        or else the state encodings produced by functions in our library
        could violate the "no duplicates" invariant of the state set.

        Args:
            *args: information to be encoded as a state name.

        Return:
            str: a name that encodes the values of the arguments.
        """
        return f"<{"; ".join(map(str, args))}>"
    
    def is_trim_but_empty(self):
        """A helper function that checks
        whether an FST is the edge case of the trimmedness condition.
        That is, the empty FST with one rejecting state and no transitions.

        Args:
            F (FST): the FST to be checked.
        
        Returns:
            bool: whether the FST has one rejecting state and no transitions.
        """
        return len(self.Q) == 1 and len(self.E) == 0 and len(self.stout) == 0
    
def new_rejector(Sigma, Gamma):
    """Creates an FST that rejects every string pair.
    
    Ensures:
        trimmedness
        final-output emptiness
        input-string expansion
        determinism

    Args:
        Sigma (list): the input alphabet.
        Gamma (list): the output alphabet.
    
    Returns:
        FST: the rejector FST.
    """
    # initialize the new FST
    F = FST(Sigma, Gamma)
    F.name = "rejector-FST"
    F.Q, F.E, F.qe, F.stout = ["q"], [], "q", {}

    return F

def new_acceptor(Sigma, Gamma):
    """Creates an FST that accepts every string pair.
    
    Ensures:
        trimmedness
        final-output emptiness
        input-string expansion

    Args:
        Sigma (list): the input alphabet.
        Gamma (list): the output alphabet.
    
    Returns:
        FST: the acceptor FST.
    """
    # initialize the new FST
    F = FST(Sigma, Gamma)
    F.name = "acceptor-FST"
    F.Q, F.E, F.qe, F.stout = ["q"], [], "q", {"q" : ""}

    # add transitions that allow writing any character to input or output
    for c in Sigma:
        F.E.append(["q", c, "", "q"])
    for c in Gamma:
        F.E.append(["q", "", c, "q"])

    return F

def new_identity(Sigma):
    """Creates an FST that recognizes the identity function.
    
    Ensures:
        trimmedness
        final-output emptiness
        input-string expansion
        determinism

    Args:
        Sigma (list): the input alphabet.
    
    Returns:
        FST: the identity FST.
    """
    # initialize the new FST
    F = FST(Sigma, Sigma)
    F.name = "identity-FST"
    F.Q, F.E, F.qe, F.stout = ["q"], [], "q", {"q" : ""}

    # add transitions that allow copying any character from input to output
    for c in Sigma:
        F.E.append(["q", c, c, "q"])

    return F

def domain(F):
    """Given an FST recognizing a relation `R`,
    returns an FST recognizing the relation `{ (u, u) | ∃ w, (w, u) ∈ R }`.

    Invariants:
        trimmedness
        input-string expansion
        determinism

    Args:
        F (FST): the original FST.
    
    Returns:
        FST: an FST that recognizes its domain.
    """
    # initialize the new FST
    G = F.copy_fst()
    G.name = f"dom({F.name})"

    # copy the input string transition of every transition to its output
    for tr in G.E:
        tr[2] = tr[1]

    # empty the output strings on final transitions
    for q in G.stout.keys():
        G.stout[q] = ""
    
    return G

def image(F):
    """Given an FST recognizing a relation `R`,
    returns an FST recognizing the relation `{ (u, u) | ∃ w, (u, w) ∈ R }`.

    Ensures:
        final-output emptiness
    
    Invariants:
        trimmedness

    Args:
        F (FST): the original FST.
    
    Returns:
        FST: an FST that recognizes its image.
    """
    # initialize the new FST
    # we need final outputs to be empty because the FST class does not support final inputs
    G = expand_final(F)
    G.name = f"img({F.name})"

    # copy the output string transition of every transition to its input
    for tr in G.E:
        tr[1] = tr[2]
    
    return G

def trim_inaccessible(F):
    """Removes states and transitions from the FST
    that are not accessible from the initial state.

    Invariants:
        trimmedness
        final-output emptiness
        input-string expansion
        determinism

    Args:
        F (FST): the original FST.

    Returns:
        FST: the trimmed FST.
    """
    # initialize the new FST
    G = FST(deepcopy(F.Sigma), deepcopy(F.Gamma))
    G.name = f"trim_inaccessible({F})"
    Q_set, E_set, G.qe, G.stout = set(), set(), F.qe, {}

    # perform a breadth-first traversal of the original FST from the initial state
    worklist = Queue()
    worklist.put(F.qe)
    while not worklist.empty():
        curr_q = worklist.get()
        if curr_q not in Q_set:
            Q_set.add(curr_q)
            for [q, u, v, q_] in F.E:
                if curr_q == q:
                    E_set.add((q, u, v, q_))
                    worklist.put(q_)

    # copy over the final outputs of the states that remain
    for q, w in F.stout.items():
        if q in Q_set:
            G.stout[q] = w

    G.Q, G.E = list(Q_set), list(map(list, E_set))
    return G

def trim_useless(F):
    """Removes states and transitions from the FST
    from which no accepting state is accessible,
    except for the initial state, which is not allowed to be removed.

    Invariants:
        trimmedness
        final-output emptiness
        input-string expansion
        determinism

    Args:
        F (FST): the original FST.

    Returns:
        FST: the trimmed FST.
    """
    # initialize the new FST
    G = FST(deepcopy(F.Sigma), deepcopy(F.Gamma))
    G.name = f"trim_useless({F})"
    Q_set, E_set, G.qe, G.stout = set(), set(), F.qe, {}

    # perform a breadth-first traversal of the original FST from the accepting states
    worklist = Queue()
    for q in F.stout.keys():
        worklist.put(q)
    while not worklist.empty():
        curr_q_ = worklist.get()
        if curr_q_ not in Q_set:
            Q_set.add(curr_q_)
            for [q, u, v, q_] in F.E:
                if curr_q_ == q_:
                    E_set.add((q, u, v, q_))
                    worklist.put(q)

    # add back the initial state if it was not traversed already
    Q_set.add(G.qe)

    # copy over the final outputs of the states that remain
    for q, w in F.stout.items():
        if q in Q_set:
            G.stout[q] = w

    G.Q, G.E = list(Q_set), list(map(list, E_set))
    return G

def trim(F):
    """Removes states and transitions from the FST
    that are never traversed by an accepting run.

    Ensures:
        trimmedness

    Invariants:
        final-output emptiness
        input-string expansion
        determinism

    Args:
        F (FST): the original FST.

    Returns:
        FST: the trimmed FST.
    """
    G = trim_useless(trim_inaccessible(F))
    G.name = f"trim({F})"

    return G

def is_empty(F):
    """Checks that the FST accepts no string pairs.

    Args:
        F (FST): the target FST.

    Returns:
        bool: `True` iff there is no string pair that `F` accepts.
    """
    return trim(F).is_trim_but_empty()

def expand_inputs(F):
    """Expands transitions with multi-character input strings
    into non-accepting chains of transitions with single-character input strings.

    Ensures:
        input-string expansion

    Invariants:
        trimmedness
        final-output emptiness
        determinism

    Args:
        F (FST): the original FST.
    
    Returns:
        FST: an FST that accepts the same relation but has no multi-character input strings.
    """
    # initialize the new FST
    G = FST(deepcopy(F.Sigma), deepcopy(F.Gamma))
    G.name = f"expand_inputs({F})"
    Q_set, E_set, G.qe, G.stout = set(), set(), FST.encode_state(F.qe, ""), {}

    # Construct the new set of states and transitions.
    # Every state `q` is mapped to many new states `<q; u>`,
    # where `u` ranges over prefixes of the outgoing input strings from `q`.
    # Every transition `[q, u, v, q']` is mapped to a series of new transitions
    # of the form `[<q; w>, c, "", <q; wc>]`, where `wc` is an incomplete prefix of `u`,
    # along with the completing transition `[<q; w>, c, v, <q'; "">]`, where `wc` equals `u`.
    for q in F.Q:
        Q_set.add(FST.encode_state(q, ""))
    for [q, u, v, q_] in F.E:
        for i in range(1, len(u)):
            Q_set.add(FST.encode_state(q, u[:i]))
            E_set.add((FST.encode_state(q, u[:i-1]), u[i-1], "", FST.encode_state(q, u[:i])))
        E_set.add((FST.encode_state(q, u[:-1]), u[-1:], v, FST.encode_state(q_, "")))

    # copy over the final outputs
    for q, w in F.stout.items():
        G.stout[FST.encode_state(q, "")] = w

    G.Q, G.E = list(Q_set), list(map(list, E_set))
    return G

def expand_final(F):
    """Expands final states with nonempty output strings
    into a non-accepting state with a transition to a new accepting state.

    Ensures:
        final-output emptiness

    Invariants:
        trimmedness
        input-string expansion
        determinism IF already final-output empty

    Args:
        F (FST): the original FST.
    
    Returns:
        FST: an FST that accepts the same relation but has no nonempty final outputs.
    """
    # initialize the new FST
    G = FST(deepcopy(F.Sigma), deepcopy(F.Gamma))
    G.name = f"expand_final({F})"
    G.Q, G.E, G.qe, G.stout = deepcopy(F.Q), deepcopy(F.E), F.qe, {}

    # account for nonempty final outputs by turning them into transitions to new accepting states,
    # if empty then just copy the final output verbatim
    for q, w in F.stout.items():
        if w == "":
            G.stout[q] = ""
        else:
            G.Q.append(q_ := G.fresh_state(q))
            G.E.append([q, "", w, q_])
            G.stout[q_] = ""

    return G

def invert(F):
    """Given an FST that accepts the relation `R`,
    returns an FST that accepts the relation `{ (u, v) | (v, u) ∈ R }`.

    Ensures:
        final-output emptiness

    Invariants:
        trimmedness

    Args:
        F (FST): the original FST.

    Returns:
        FST: the inverted FST.
    """
    # we need final outputs to be empty because the FST class does not support final inputs
    F_name = F.name
    F = expand_final(F)

    # initialize the new FST
    G = FST(deepcopy(F.Sigma), deepcopy(F.Gamma))
    G.name = f"{F_name}⁻¹"
    G.Q, G.E, G.qe, G.stout = deepcopy(F.Q), [], F.qe, deepcopy(F.stout)

    # copy over the transitions with swapped input an output strings
    for [q, u, v, q_] in F.E:
        G.E.append([q, v, u, q_])

    return G

def concatenate(F, G):
    """Given FSTs that accept the relations `RF` and `RG`, respectively,
    returns an FST that accepts the relation `RF · RG`.
    That is, the relation of all string pairs that are the result of
    concatenating a string pair from `RF` to a string pair from `RG`.

    Invariants:
        trimmedness IF both nonempty
        final-output emptiness
        input-string expansion

    Args:
        F (FST): the left-hand original FST.
        G (FST): the right-hand original FST.

    Returns:
        FST: the concatenation FST.
    """
    # we need final outputs of the first machine to be empty
    # so that we do not miss output upon traversal to the next machine
    F_name = F.name
    F = expand_final(F)

    # initialize the new FST
    H = FST(list(set(F.Sigma) | set(G.Sigma)), list(set(F.Gamma) | set(G.Gamma)))
    H.name = f"({F_name} · {G})"
    H.Q, H.E, H.qe, H.stout = [], [], FST.encode_state("LEFT", F.qe), {}

    # copy over the states from both `F` and `G`
    for qf in F.Q:
        H.Q.append(FST.encode_state("LEFT", qf))
    for qg in G.Q:
        H.Q.append(FST.encode_state("RIGHT", qg))

    # copy over the transitions from both `F` and `G`
    for [qf, u, v, qf_] in F.E:
        H.E.append([FST.encode_state("LEFT", qf), u, v, FST.encode_state("LEFT", qf_)])
    for [qg, u, v, qg_] in G.E:
        H.E.append([FST.encode_state("RIGHT", qg), u, v, FST.encode_state("RIGHT", qg_)])

    # for every final state,
    # create an epsilon transition to nondeterministically begin running the next machine
    for qf in F.stout.keys():
        H.E.append([FST.encode_state("LEFT", qf), "", "", FST.encode_state("RIGHT", G.qe)])
    
    # copy over the final transitions of the other machine
    for qg, w in G.stout.items():
        H.stout[FST.encode_state("RIGHT", qg)] = w

    return H

def kleene_closure(F):
    """Given an FST that accepts the relation `R`,
    returns an FST that accepts the relation `R*`.
    That is, the relation of all string pairs that are the result of
    concatenating many string pairs from `R`.

    Ensures:
        final-output emptiness
    
    Invariants:
        trimmedness IF nonempty
        input-string expansion

    Args:
        F (FST): the original FST.
    
    Returns:
        FST: the kleene-closure FST.
    """
    # we need final outputs to be empty
    # so that we do not miss output upon traversal back to the initial state
    F_name = F.name
    F = expand_final(F)

    # initialize the new FST
    G = FST(deepcopy(F.Sigma), deepcopy(F.Gamma))
    G.name = f"{F_name}*"
    G.Q, G.E, G.qe, G.stout = deepcopy(F.Q), deepcopy(F.E), F.qe, deepcopy(F.stout)

    # for every final state,
    # create an epsilon transition to nondeterministically return to the initial state
    for q in G.stout.keys():
        tr = [q, "", "", G.qe]
        if tr not in G.E:
            G.E.append(tr)

    return G

def union(F, G):
    """Given FSTs that accept the relations `RF` and `RG`, respectively,
    returns an FST that accepts the relation `RF ∪ RG`.

    Invariants:
        trimmedness IF both nonempty
        final-output emptiness
        input-string expansion

    Args:
        F (FST): the left-hand original FST.
        G (FST): the right-hand original FST.

    Returns:
        FST: the union FST.
    """
    # initialize the new FST
    H = FST(list(set(F.Sigma) | set(G.Sigma)), list(set(F.Gamma) | set(G.Gamma)))
    H.name = f"({F} ∪ {G})"
    H.Q, H.E, H.qe, H.stout = [], [], FST.encode_state("LEFT", F.qe), {}

    # create an epsilon transition to nondeterministically choose between running `F` and `G`
    H.E.append([FST.encode_state("LEFT", F.qe), "", "", FST.encode_state("RIGHT", G.qe)])

    # copy over the states from both `F` and `G`
    for qf in F.Q:
        H.Q.append(FST.encode_state("LEFT", qf))
    for qg in G.Q:
        H.Q.append(FST.encode_state("RIGHT", qg))

    # copy over the transitions from both `F` and `G`
    for [qf, u, v, qf_] in F.E:
        H.E.append([FST.encode_state("LEFT", qf), u, v, FST.encode_state("LEFT", qf_)])
    for [qg, u, v, qg_] in G.E:
        H.E.append([FST.encode_state("RIGHT", qg), u, v, FST.encode_state("RIGHT", qg_)])

    # copy over the final outputs from both `F` and `G`
    for qf, w in F.stout.items():
        H.stout[FST.encode_state("LEFT", qf)] = w
    for qg, w in G.stout.items():
        H.stout[FST.encode_state("RIGHT", qg)] = w

    return H

def consume_input_from(F, u, qs):
    """Given a list of state-string pairs and an input string,
    runs a nondeterministic FST on the input string
    from every given state and for every possible nondeterministic choice,
    accumulating output onto the original given strings.

    To guarantee termination, transition cycles whose input strings are empty
    are not traversed for more than one consecutive loop,
    as enfored by the `visited` tracker only considering
    the state in the FST and the amount of input consumed.

    Args:
        F (FST): The target FST.
        u (str): The input string.
        qs (list[Tuple[str, str]]): A list of start state-string from which to run the FST.

    Returns
        list[Tuple[str, str]]: All possible results of running the FST.
    """
    visited = {}
    worklist = Queue()
    for q, v in qs:
        worklist.put((q, u, v))
    while not worklist.empty():
        (curr_q, curr_u, curr_v) = worklist.get()
        if (curr_q, curr_u) not in visited:
            visited[(curr_q, curr_u)] = curr_v
            for [q, u, v, q_] in F.E:
                if curr_q == q and curr_u.startswith(u):
                    worklist.put((q_, curr_u[len(u):], curr_v + v))

    return [(q, v) for ((q, u), v) in visited.items() if u == ""]

def left_epsilon_free_compose(F, G):
    """Given FSTs that accept the relations `RF` and `RG`, respectively,
    returns an FST that accepts the relation `{ (u, v) | ∃ w, (u, w) ∈ RG ∧ (w, v) ∈ RF }`.
    In the special case that `RF` and `RG` are both subsequential functions
    (which is guaranteed if both original FSTs are deterministic),
    this has the effect of typical function composition.

    Requiring the left-hand FST to have no transitions with empty input strings
    allows us to design this implementation to have determinism as an invariant.
    Additionally, this condition always holds for deterministic FSTs,
    so it will be useful for subsequential applications.

    Invariants:
        final-output emptiness
        input-string expansion
        determinism IF `G` already final-output empty

    Args:
        F (FST): the left-hand (second applied) original FST, MUST have no empty input strings.
        G (FST): the right-hand (first applied) original FST.

    Returns:
        FST: the composition FST.
    """
    # we have to expand inputs in `F` so that it never over-consumes output of `G`
    F_name = F.name
    F = expand_inputs(F)

    # expanding final outputs of the right-hand machine makes this construction far easier,
    # but it also means that determinism is not always an invariant,
    # whereas it would be in a more robust implementation
    G_name = G.name
    G = expand_final(G)

    # initialize the new FST
    H = FST(deepcopy(G.Sigma), deepcopy(F.Gamma))
    H.name = f"({F_name} ∘ {G_name})"
    Q_set, E_set, H.qe, H.stout = set(), set(), FST.encode_state(F.qe, G.qe), {}

    # perform a breadth-first traversal of the new FST
    # by traversing transitions in `G` while simulating both `G` and `F`
    worklist = Queue()
    worklist.put((F.qe, G.qe))
    while not worklist.empty():
        (curr_qf, curr_qg) = worklist.get()
        new_q = FST.encode_state(curr_qf, curr_qg)
        if new_q not in Q_set:
            Q_set.add(new_q)
            for [qg, ug, vg, qg_] in G.E:
                if curr_qg == qg:
                    for (qf_, vf) in consume_input_from(F, vg, [(curr_qf, "")]):
                        E_set.add((new_q, ug, vf, FST.encode_state(qf_, qg_)))
                        worklist.put((qf_, qg_))

    # copy over the shared final states
    for qf, w in F.stout.items():
        for qg in G.stout.keys():
            new_q = FST.encode_state(qf, qg)
            if new_q in Q_set:
                H.stout[new_q] = w

    H.Q, H.E = list(Q_set), list(map(list, E_set))
    return H

def determinize(F):
    """Turns a nondeterministic FST that recognizes a subsequential function
    into a deterministic FST that recognizes the same function.
    A deterministic FST has only single-character input strings,
    and for each state, at most one outgoing transition with every input string.

    Ensures:
        trimmedness
        input-string expansion
        determinism

    Args:
        F (FST): the original functional FST.
    
    Returns:
        FST: an FST that accepts the same function but is deterministic.
    """
    # expanding inputs in `F` means that we never have to partially traverse a transition
    # we have to trim `F` so that we get the subsequential guarantees for the whole machine
    F_name = F.name
    F = expand_inputs(trim(F))

    # the initial state of the new machine is the set of states reachable
    # from the initial state of the old machine on the empty string
    qes = sorted(consume_input_from(F, "", [(F.qe, "")]))

    # initialize the new FST
    G = FST(deepcopy(F.Sigma), deepcopy(F.Gamma))
    G.name = f"determinize({F_name})"
    Q_set, E_set, G.qe, G.stout = set(), set(), FST.encode_state(*qes), {}

    # perform a breadth-first traversal of the new FST
    # by tracking every possible nondeterministic behavior of `F` on consuming each character
    worklist = Queue()
    worklist.put(qes)
    while not worklist.empty():
        curr_qs = sorted(worklist.get())
        new_q = FST.encode_state(*curr_qs)
        if (tuple(curr_qs), new_q) not in Q_set:
            Q_set.add((tuple(curr_qs), new_q))
            for c in F.Sigma:
                qs = sorted(consume_input_from(F, c, curr_qs))
                if qs != []:
                    common_output = lcp(*[v for (_, v) in qs])
                    qs_ = [(q, v[len(common_output):]) for (q, v) in qs]
                    E_set.add((new_q, c, common_output, FST.encode_state(*qs_)))
                    worklist.put(qs_)

    # mark any state containing a final state of the original machine as a new final state
    for (qs, new_q) in Q_set:
        for (q, v) in qs:
            if q in F.stout:
                G.stout[new_q] = v
                break

    G.Q, G.E = list(map(lambda x : x[1], Q_set)), list(map(list, E_set))
    return G

def onwardize(F):
    """Pushes forward common prefixes of output strings
    so that the resulting FST produces output as early as possible.

    Ensures:
        trimmedness
    
    Invariants:
        final-output emptiness
        input-string expansion
        determinism
    
    Args:
        F (FST): the original FST.

    Returns:
        FST: an FST that recognizes the same relation but it onward.
    """
    # initialize the new FST, which we must trim to ensure termination
    G = trim(F)
    G.name = f"onwardize({F})"

    # push outputs forward until fixedpoint
    while True:

        outputs_per_state, common_output_per_state = {}, {}

        # collect all transition outputs indexed by state
        for [q, _, v , _] in G.E:
            if q not in outputs_per_state:
                outputs_per_state[q] = []
            outputs_per_state[q].append(v)
        
        # collect all final outputs indexed by state
        for q, v in G.stout.items():
            outputs_per_state[q].append(v)
        
        # compute the common prefixes of all output sets
        for (q, outputs) in outputs_per_state.items():
            common_output_per_state[q] = lcp(*outputs)
        
        # if there are no more nonempty common prefixes, then we are done
        if all([v == "" for (_, v) in common_output_per_state.items()]):
            return G
        
        # for every transition, push common output forward and recieve pushed common output
        for tr in G.E:
            tr[2] = tr[2][len(common_output_per_state[tr[0]]):] + common_output_per_state[tr[3]]

        # for every final output, push common prefix forward
        for q in G.stout.keys():
            G.stout[q] = G.stout[q][len(common_output_per_state[q]):]

def minimize(F):
    """Given a deterministic FST,
    returns the canonical FST that recognizes the same subsequential function.
    It will be trim, onward, and minimal in the sense that all states are observably distinct.

    The minimization algorithm uses Hopcroft's partition-refinement strategy
    (https://en.wikipedia.org/wiki/DFA_minimization).
    
    Ensures:
        trimmedness
        input-string expansion
        determinism
    
    Invariants:
        final-output expansion
    
    Args:
        F (FST): the original deterministic FST.
    
    Returns:
        FST: an FST that accepts the same function but is onward.
    """
    # we must onwardize the original FST
    F_name = F.name
    F = onwardize(F)

    # initialize an overly coarse partition of the states into indexed equivalance classes
    partition = None
    class_of = { q : 0 for q in F.Q }

    # refine the partition using local inferences until fixedpoint
    while True:

        # for every state and final transition,
        # collect a signature including its output and destination class
        signature_per_state_per_tr = { q: { u: None for u in [""] + F.Sigma } for q in F.Q }
        for [q, u, v, q_] in F.E:
            signature_per_state_per_tr[q][u] = (v, class_of[q_])
        for q, v in F.stout.items():
            signature_per_state_per_tr[q][""] = v

        # construct a signature of observable information per state
        signature_per_state = { q: (
            class_of[q],
            tuple(signature_per_state_per_tr[q][u] for u in [""] + F.Sigma)
        ) for q in F.Q }

        old_partition = partition

        # "transpose" the state signatures by keying sets of nondistinct states by their signature
        partition = {}
        for (q, sig) in signature_per_state.items():
            if sig not in partition:
                partition[sig] = set()
            partition[sig].add(q)

        class_of = { q: i for (i, (_, s)) in enumerate(partition.items()) for q in s }

        # if there was no change, then we are done with the refinement
        if partition == old_partition:
            break
    
    # initialize the new FST
    G = FST(deepcopy(F.Sigma), deepcopy(F.Gamma))
    G.name = f"minimize({F_name})"
    G.E, G.stout = [], {}
    G.Q = [str(sig[0]) for sig in partition.keys()]
    G.qe = str(next(sig for (sig, s) in partition.items() if F.qe in s)[0])

    # populate the state and final transitions by reading from the signatures of the partition
    for sig in partition.keys():
        if sig[1][0] != None:
            G.stout[str(sig[0])] = str(sig[1][0])
        for (i, u) in zip(range(1, len(F.Sigma) + 1), F.Sigma):
            if sig[1][i] != None:
                G.E.append([str(sig[0]), u, sig[1][i][0], str(sig[1][i][1])])
    
    return G
