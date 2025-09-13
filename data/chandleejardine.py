Data = [
    ("1", "tad"),
    ("2", "tat"),
    ("3", "tada"),
    ("1A", "tadda"),
    ("2A", "tatta"),
    ("3A", "tadata"),
    ("1B", "tadda"),
    ("2B", "tatda"),
    ("3B", "tadada"),
    
	]

Sigma = ["1", "2", "3", "A", "B"]
Gamma = ["t", "a", "d"]

data_new_format = [
    (('root1',), ('t', 'a', 'dx')),
    (('root2',), ('t', 'a', 't')),
    (("root3",), ('t', 'a', 'dx', 'a')),
    (("root1", 'suff1'), ('t', 'a', 'dx', 'dx', 'a')),
    (("root2", 'suff1'), ('t', 'a', 't', 't', 'a')),
    (("root3", 'suff1'), ('t', 'a', 'dx', 'a', 't', 'a')),
    (("root1", 'suff2'), ('t', 'a', 'dx', 'dx', 'a')),
    (("root2", 'suff2'), ('t', 'a', 't','dx', 'a')),
    (("root3", 'suff2'), ('t', 'a', 'dx', 'a', 'dx', 'a')),
]

sigma_new_format = ['root1', 'root2', 'root3', 'suff1', 'suff2']
gamma_new_format = ['t', 'a', 'dx']
