from fst_object import *
from dfa_object import *
from helper import *
from si2dla_new import *
from itertools import product


# implementation of GOV, 90
# builds a DFA that can recognize the language of R 
def k_tssi(k, R):

    r_symbols = set(alphabetize(R))
    i_k = get_k_prefixes(k, R)
    f_k = get_k_suffixes(k, R)
    t_k = non_appearing(k, R)
    alphabets, k_prefixes, k_suffixes, prohibited = (r_symbols, i_k, f_k, t_k)
    T = DFA()
    T.Sigma = alphabets
    T.Q = set('0')
    T.qe = '0'
    T.E = set()
    T.qf = set()

    for prefix_substring in k_prefixes:
        for j in range(0, len(prefix_substring)):
            T.Q.add(prefix_substring[0: j+1])
            if j == 0:
                T.E.add(("0", prefix_substring[j], "", prefix_substring[j]))
            else:
                T.E.add((prefix_substring[0:j], prefix_substring[j], "", prefix_substring[0: j+1]))

    
    combined_alphabet = "".join(alphabets)

    k_permutations = get_k_permutations(k, combined_alphabet)

    difference = k_permutations - prohibited


    for substring in difference:
        T.Q.add(substring[1:k])
        T.E.add((substring[0:k-1], substring[k-1], "", substring[1:k]))
    

    T.qf = T.qf | k_suffixes

    return T    
  


# get all prefixes of length k
def get_k_prefixes(k, R):
    prefixes = set()
    for word in R:
        prefix = word[0:k-1]
        prefixes.add(prefix)
    return prefixes

# get all suffixes of length k
def get_k_suffixes(k, R):
    suffixes = set()
    for word in R:
        suffix = word[-(k-1):]
        suffixes.add(suffix)
    return suffixes


# get all possible substrings with given symbols and length k
def get_k_permutations(k, symbols):
    return set([''.join(x) for x in product(symbols, repeat=k)])

# compute all prohibited substrings
def non_appearing(k, R):

    r_symbols = set(alphabetize(R))

    combined_symbols = "".join(r_symbols)

    #permute all possible strings of length k over r_symbols (thx stackoverflow)
    permutations = get_k_permutations(k, combined_symbols)

    # geeks4geeks coming in clutch
    # get all substrings of length k
    all_substrings = set()
    for string in R:
        substring = set([string[i:i+k] for i in range(len(string) - k + 1)])
        all_substrings = all_substrings | substring

    # print(permutations)
    # print(all_substrings)
    
    #prohibited substrings are the difference b/w all possible substrings of length k and all substrings of length k
    prohibited = permutations - all_substrings

    return prohibited
    

# hoopcroft's DFA minimization algorithm; see https://en.wikipedia.org/wiki/DFA_minimization for pseudocode
# returns a set of all non-distinct states
def minimize_dfa(T):
    P = set()
    P.add(frozenset(T.qf))
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
                        if len(X & Y ) <= len(Y - X):
                            W.add(frozenset(X & Y))
                        else:
                            W.add(frozenset(Y - X))
                else:
                    temp_P.add(Y)
            P = temp_P

    return P


# function to minimize the dfa and convert it into an fst
# this is hilariously bad code, needs to be rewritten 
def minimize_dfa_to_fst(T):
    P = minimize_dfa(T)
    print(P)

    new_T = FST()

    new_T.Q = []
    new_T.qe = T.qe
    new_T.E = set()
    
    state_name = 1
    merged_states = {}

    states_in_order = {}
    for eq_state in P:
        eq_state = set(eq_state)
        if new_T.qe in eq_state:
            merged_states['0'] = eq_state
            new_T.Q.append('0')
        else:
            merged_states[str(state_name)] = eq_state
            new_T.Q.append(str(state_name))
            state_name += 1

    merged_states_reverse = {str(v): k for k, v in merged_states.items()}

    for eq_state in P:
        source_states = set()
        eq_state = set(eq_state)
        for tr in T.E:
            if tr[3] in eq_state:
                for state in merged_states:
                    if tr[0] in merged_states[state]:
                        # print("passed")
                        #print(f"{tr[3]}:  {tr[0]}")
                        source_states.add(state)
            
                for source in source_states:
                    new_T.E.add((source, tr[3], 'x', merged_states_reverse[str(eq_state)]))

    new_T.E = list(new_T.E)


    return new_T



morphology = ["1", "2", "3", "1A", "2A", "3A", "1B", "2B", "3B"]
k = 2
domain = k_tssi(k, morphology)

# print(domain.E)

domain = minimize_dfa_to_fst(domain)


D3 = [("1", "tad"),
    ("2", "tat"),
    ("3", "tada"),
    ("1A", "tadda"),
    ("2A", "tatta"),
    ("3A", "tadata"),
    ("1B", "tadda"),
    ("2B", "tatda"),
    ("3B", "tadada")
	]

R3 = ["1", "2", "3", "A", "B"]
S3 = ["t", "a", "d"]


D = FST(["1", "2", "3", "A", "B"])
D.Q = ["0", "1", "2"]
D.qe = "0"
D.E = [("0", "1", "x", "1"), ("0", "2", "x", "1"), ("0", "3", "x", "1"), ("1", "A", "x", "2"), ("1", "B", "x", "2")]

print(f"Manual: {D.Q}")
print(f"Inferred: {domain.Q}")

print(f"Manual: {D.qe}")
print(f"Inferred: {domain.qe}")


print(f"Manual Domain: {D.E}")
print(f"Inferred Domain: {domain.E}")


# T_f, T_g = si2dla_ex(D,D3,R3,S3)

T_f, T_g = si2dla_ex(domain,D3,R3,S3)
