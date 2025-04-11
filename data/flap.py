""" American English Flapping

"""

Data = [
	("", ""),
# 4^1
	("A", "ta"),
	("B", "t"),
	("C", "a"),
	("D", "ara"),
# 4^2
	("AA", "tara"),
	#("AB", "tat"), #*
	#("AC", "taa"), #*
	#("AD", "taara"),

	#("BA", "tta"),
	#("BB", "tt"), #*
	#("BC", "ta"), #*
	#("BD", "tara"), #*

	("CA", "ara"),
	("CB", "at"),
	#("CC", "aa"), #*
	#("CD", "aara"), #*

	#("DA", "arara"),
	#("DB", "arat"), #*
	#("DC", "araa"), #*
	#("DD", "araara"), #*
# 4^3
	("CBC", "ara"),
	#("CBA", "atta"),
	#("CBB", "att"),
	#("AAA", "tarara"),
	#("ABA", "tatta"),
	#("ACA", "taara"),
	#("ADA", "taarara"),

	#("CBC", "ara"),
	#("CDCA", "arara"),
	];
Sigma = ["A", "B", "C", "D"];
Gamma = ["a", "t", "d", "r"];
