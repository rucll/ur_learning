# Modified version of Figure 1 from Hua & Jardine 2021 to exhibit all 4 modes of opacity
Data = [
	("",""),
	("a", "a"),
	("b", "b"),
	("c", "c"),
	("w", "aa"),
	("x", "caa"),
	("y", "aac"),
	("z", "caac"),

	("aa", "aa"),
	("ab", "aa"),
	("ca", "ca"),
	("wb", "aab"),
];


data_new_format = [
    (("a",), ("a",)),
	(("b",), ("b",)),
	(("c",), ("c",)),
	(("w",), ('a', 'a')),
	(("x",), ("c", "a", "a",)),
	(("y",), ("a", "a", "c")),
	(("z",), ("c", "a", "a", "c",)),

	(("a", "a"), ("a", "a")),
	(("a", "b"), ("a", "a")),
	(("c", "a"), ("c", "a")),
	(("w", "b"), ("a", "a", "b")),
]

sigma_new_format = ["a", "b", "c", "w","x","y","z"];
gamma_new_format = ["a","b","c"];