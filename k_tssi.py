from dfa_object import *
from helper import *
from itertools import product

# implementation of GOV, 90
# builds a DFA that can recognize the language of R based on
# alphabets: the alphabet of R
# k_prefixes: all prefixes of length k-1 
# k_suffixes: all suffixes of length k-1
# prohibited: all strings of length k that are not allowed in R
def k_tssi(k, R):

    r_symbols = set(alphabetize(R))
    i_k = get_k_prefixes(k, R)
    f_k = get_k_suffixes(k, R)
    t_k = non_appearing(k, R)
    alphabets, k_prefixes, k_suffixes, prohibted = (r_symbols, i_k, f_k, t_k)
    T = DFA()
    T.Sigma = alphabets
    T.Q = set('')
    T.qe = ''
    T.E = set()
    T.qf = set()

    # build the dfa consisting of just k-1 length strings
    for prefix_substring in k_prefixes:
        for j in range(0, len(prefix_substring)):
            T.Q.add(prefix_substring[0: j+1])
            if j == 0:
                T.E.add(("", prefix_substring[j], "", prefix_substring[j]))
            else:
                T.E.add((prefix_substring[0:j], prefix_substring[j], "", prefix_substring[0: j+1]))


    combined_alphabet = "".join(alphabets)

    k_permutations = get_k_alphabet_combinations(k, combined_alphabet)

    difference = k_permutations - prohibted

    # complete the dfa by adding the allowed strings of length k
    for substring in difference:
        T.Q.add(substring[1:k])
        T.E.add((substring[0:k-1], substring[k-1], "", substring[1:k]))
    

    T.qf = T.qf | k_suffixes

    return T    
  


# get all prefixes of length k-1
def get_k_prefixes(k, R):
    prefixes = set()
    for word in R:
        prefix = word[0:k-1]
        prefixes.add(prefix)
    return prefixes

# get all suffixes of length k-1
def get_k_suffixes(k, R):
    suffixes = set()
    for word in R:
        suffix = word[-(k-1):]
        suffixes.add(suffix)
    return suffixes


# get all possible substrings with given symbols of length k
def get_k_alphabet_combinations(k, combined_alphabet):
    return set([''.join(x) for x in product(combined_alphabet, repeat=k)])

# get all prohibited substrings
def non_appearing(k, R):

    r_alphabet = set(alphabetize(R))

    combined_alphabet = "".join(r_alphabet)

    # get all possible substrings of length k over the alphabet of R (thx stackoverflow)
    all_k_alphabet_substrings = get_k_alphabet_combinations(k, combined_alphabet)

    # get all substrings of length k in R
    all_k_R_substrings = set()
    for string in R:
        substring = set([string[i:i+k] for i in range(len(string) - k + 1)])
        all_k_R_substrings = all_k_R_substrings | substring

    # prohibited substrings is the difference b/w all possible k substrings over the alphabet of R and all possible k substrings over R
    prohibited = all_k_alphabet_substrings - all_k_R_substrings

    return prohibited