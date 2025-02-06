# Vowel Elision in Sri Lankan Creole
# from Smith (1978), ex. 554
# the domain and range of f are given as natural classes

# [V +back -long -stress] -> λ / _#V
"""
    /te:#a:w / -> [teyá*w]
    (tea water) (tea)
"""

# Offgliding (555)
"""
    λ -> [-syll -cons -high] / [V -back -low]_[C +son -nas -ant]

    a) /de:r/ -> [dé:ər] 'daily'
    b) /prum+e:r/ -> [prumé+ər] 'first'
    c) /osi:r/ -> [osí+ər] 'he/she HON'

    offglide: G
    non-back non-low vowel: 1
    /r/: R <=> [C +son -nas -ant]
    non-specifics (note same results for more specific classification):
    consonant: C
    vowel: V
"""

"""note;
    if you assume an intermediate alphabet Rho,
    then we could say that d -> C -> d, etc.
    would IDLA correctly learn this?

    The issue is primarily of data; if we are designing the rule
    on the basis of natural classes, it's unreasonable to expect
    IDLA to infer this grouping without a dataset which
    demonstrates the difference.

    A further area of study would be extending IDLA
    to derive phonological rules specific to natural classes
"""

D = [
    ("d", "d"), ("p", "p"), ("m", "m"), ("s", "s"),
    ("u", "u"), ("o", "o"),
    ("1", "1"),
    ("r", "r"),
    ("d1r", "d1Gr"), # (a)
    ("prum1r", "prum1Gr"), # (b)
    ("os1r", "os1Gr")  # (c)
]

S = ["d", "p", "r", "u", "o", "1", "m", "s"];
R = S.append("G");
