# Example 1 from Hua & Jardine 2021
Data = [
	# ("",""),
	("w","aa"),
	("x","cbcb"),
	("y","bc"),
	("z","bca"),
	("ww","aaaa"),
	("wx", "aacbcb"),
	("wy", "aabc"),
	("wz", "aabca"),
	("xw", "cbcbaa"),
	("xx", "cbcbcbcb"),
	("xy", "cbcbbc"),
	("xz", "cbcbbca"),
	("yw", "bcaa"),
	("yx", "bccbcb"),
	("yy", "bcbc"),
	("yz", "bcbca"),
	("zw", "bcaaa"),
	("zx", "bcacbcb"),
	("zy", "bcaac"),
	("zz", "bcaaca"),
    # ("zzz", "bcaacabca")
];

Sigma = ["w","x","y","z"];
Gamma = ["a","b","c"];


data_new_format = [
    (('w',), ('a', 'a')),
	(('x',), ('c', 'b', 'c', 'b')), 
    (('y',), ('b', 'c')), 
    (('z',), ('b', 'c', 'a')), 
    (('w', 'w'), ('a', 'a', 'a', 'a')), 
    (('w', 'x'), ('a', 'a', 'c', 'b', 'c', 'b')), 
    (('w', 'y'), ('a', 'a', 'b', 'c')), 
    (('w', 'z'), ('a', 'a', 'b', 'c', 'a')), 
    (('x', 'w'), ('c', 'b', 'c', 'b', 'a', 'a')), 
    (('x', 'x'), ('c', 'b', 'c', 'b', 'c', 'b', 'c', 'b')), 
    (('x', 'y'), ('c', 'b', 'c', 'b', 'b', 'c')), 
    (('x', 'z'), ('c', 'b', 'c', 'b', 'b', 'c', 'a')), 
    (('y', 'w'), ('b', 'c', 'a', 'a')), 
    (('y', 'x'), ('b', 'c', 'c', 'b', 'c', 'b')), 
    (('y', 'y'), ('b', 'c', 'b', 'c')), 
    (('y', 'z'), ('b', 'c', 'b', 'c', 'a')), 
    (('z', 'w'), ('b', 'c', 'a', 'a', 'a')), 
    (('z', 'x'), ('b', 'c', 'a', 'c', 'b', 'c', 'b')), 
    (('z', 'y'), ('b', 'c', 'a', 'a', 'c')), 
    (('z', 'z'), ('b', 'c', 'a', 'a', 'c', 'a'))
]

sigma_new_format = ["w","x","y","z"];
gamma_new_format = ["a","b","c"];