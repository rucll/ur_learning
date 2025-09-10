from k_tssi import k_tssi
from fst_object import FST

# main function for domain inference
def infer_domain(data, k=2):
    morphemes = []
    for morphs, _ in data:
        morphemes.append(morphs)
    
    init_dfa = k_tssi(k, morphemes)

    domain = minimize_dfa_to_fst(init_dfa)

     # if there are 2 states in domain inference, then the domain is Sigma star
    if len(domain.Q) == 2:
        sigma_star = []

        for tr in domain.E:
            if tr[0] != 0:
                sigma_star.append(tr)

        domain.E = sigma_star
        domain.Q.remove(0)

    return domain

# minimize the dfa and convert it into an fst; this is probably not even needed for ostia_d
def minimize_dfa_to_fst(T):
    P = minimize_dfa(T)
    if frozenset() in P: # empty set = lambda so it can be removed from P
        P.remove(frozenset())

    # initialize FST object
    new_T = FST()   
    new_T.Q = [0]
    new_T.Sigma = list(T.Sigma)
    new_T.Gamma = ['x']
    new_T.qe = 0 # map start state to 0
    new_T.E = set() # initialize as a set because it won't add duplicate transitions later

    # group each equivalent state to one representative state
    state_name = 1
    merged_states = {}
    merged_states[''] = new_T.qe # map lambda state to start state
    for eq_state in P:
        for state in eq_state:
            if state != '':
                merged_states[state] = state_name
        new_T.Q.append(state_name)
        state_name += 1

    # create new state transitions by using representative state mappings
    for tr in T.E: 
        source_state = tr[0]
        input_symbol = tr[1]
        dest_state = tr[3]
        source_state_rep = merged_states[source_state] 
        dest_state_rep = merged_states[dest_state] 
        new_T.E.add((source_state_rep, input_symbol, 'x', dest_state_rep))
 
    new_T.E = list(new_T.E)

    return new_T


# hopcroft's DFA minimization algorithm for non-distinct states; see https://en.wikipedia.org/wiki/DFA_minimization for pseudocode
# returns a set of sets of all non-distinct states
def minimize_dfa(T):
    P = set()
    P.add(frozenset(T.qf)) # frozenset needed to add elements that are a set
    P.add(frozenset(T.Q - T.qf))

    W = set()
    W.add(frozenset(T.qf))
    W.add(frozenset(T.Q - T.qf))
    while len(W) != 0:
        A = W.pop()
        for c in T.Sigma:
            X = set()
            for tr in T.E:
                if tr[1] == c and tr[3] in A:
                    X.add(tr[0])

            temp_P = set()
            for Y in P:
                if len(X & Y) != 0 and len(Y - X) != 0:
                    # P.remove(Y)
                    temp_P.add(frozenset(X & Y))
                    temp_P.add(frozenset(Y - X))
                    if Y in W:
                        W.remove(Y)
                        W.add(frozenset(X & Y))
                        W.add(frozenset(Y - X))
                    else:
                        if len(X & Y) <= len(Y - X):
                            W.add(frozenset(X & Y))
                        else:
                            W.add(frozenset(Y - X))
                else:
                    temp_P.add(Y)
            P = temp_P

    return P