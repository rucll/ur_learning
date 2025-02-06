"""An implementation of the IDLA (To Aleftcxtear)

Written by Ben Evans
"""
from fst_object import *
from ostia import *
from helper import *

""" prefixes of a string
	w (str): subject string
	i (int): [optional] start index
	Returns:
		(set): the set of prefixes of the given string.
"""
def pref(w, i = 0):
		return {w[i:j] for j in range(len(w) + 1)};
""" wedge
"""
def wedge(S):
	s = ""
	for sp in S:
		if len(sp) > len(s):
			s = sp;
	return s;
"""
	Finds the longest common prefix of an unbounded number of strings.
	Arguments:
		S: a set of strings;
	Returns:
		(str): a longest common prefix of the input strings.
"""
def lcp(S):
	Sp = set();
	for w in S: # big set of prefixes
		Sp = Sp | pref(w);
	for w in S: # common set of prefixes
		Sp = Sp & pref(w);
	return wedge(Sp);

""" suffixes of a string
	w (str): subject string
	i (int): [optional] end index
	Returns:
		(set): the set of suffixes of the given string.
"""
def suff(w, i = -1):
	if (i == -1):
			i = len(w);
	return {w[j:i] for j in range(len(w) + 1)};

""" Longest Common Suffix
	S: set of subject strings
	Returns:
		(str): longest common suffix
"""
def lcs(S):
	l = ""; # longest suffix
	Sp = set();
	for w in S: # big set of suffixes
		Sp = Sp | suff(w);
	for w in S: # common set of suffixes
		Sp = Sp & suff(w);

	for s in Sp:
		if len(s) > len(l):
			l = s;
	return l;

""" Longest Unique Prefix
	S: set of subject strings
	s: target string
	Returns:
		(str): longest unique prefix
"""
def lup(s, S):
	return s.removesuffix(lcs(S));

def lus(s, S):
	return s.removeprefix(lcp(S));

""" Hypothesis Function
	e (edge):	   subject edge
	stout (dict):   state output
	Returns:
		(str): Hypothesis form
"""
def somega(stout, e):
	q = str(e[0]);
	v = str(e[2]);
	qp = str(e[3]);
	return v.removeprefix(stout[q]) + stout[qp];

""" Signature of a state
	S: Dict of signatures
	T: Transducer
	q: subject state
	Returns:
		(str): State signature
"""
def sig(T, q):
	if q == T.qe:
		return "";
	I = set(); # set of all incoming transitions
	for e in T.E: # of form (r, u, v, q)
		if q != e[3] or q == e[0]:
			continue;
		# we are on a relevant edge
		I.add(sig(T, e[0]) + somega(T.stout, e));
	return lcs(I);

def construct_fh(T_gf):
	T_gf.ET = set();
	fh = {};

	# collect terminals
	for e in T_gf.E:
		si = sig(T_gf, e[0]);
		sj = sig(T_gf, e[3]);
		if si != "" and lcs({si, sj}) != si:
			T_gf.ET.add(e);
		else:
			if e[1] not in fh:
				fh[e[1]] = somega(T_gf.stout, e);
	return fh;

def construct_Tg(T_gf, fh):
	# determine alternating terminals
	T_gf.ETA = set();
	T_gf.ETN = set();

	# collecting
	prefixes = set(); # prelude
	suffixes = set(); # s_{d - 1}
	underlying = None; # alternate
	surface = None; # alternated to...
	for edge in T_gf.ET:
		sm = somega(T_gf.stout, edge);
		se = T_gf.stout[edge[0]] + fh[edge[1]];
		if T_gf.stout[edge[0]] + sm != se: # then is an alternating terminal
			T_gf.ETA.add(edge);
			complete_suffix = T_gf.stout[edge[0]] + fh[edge[1]];
			suffix = lcs({complete_suffix, edge[2]});

			if underlying is None:
				underlying = complete_suffix.removesuffix(suffix);
			if surface is None:
				surface = sm.removesuffix(suffix);

			prefix = sig(T_gf, edge[0]).removesuffix(T_gf.stout[edge[0]]);
			prefixes |= (suff(prefix) - set([""]));

			suffix = edge[2].removeprefix(surface);
			suffixes |= (pref(suffix) - set([""]));

	print(f"pre-prefixes: {prefixes}");
	print(f"pre-suffixes: {suffixes}");
	T_gf.ETN = T_gf.ET - T_gf.ETA;
	for edge in T_gf.ETN:
		prefix = sig(T_gf, edge[0]).removesuffix(T_gf.stout[edge[0]]);
		prefixes -= (suff(prefix) - set([""]));

		suffix = edge[2].removeprefix(underlying);
		suffixes -= (pref(suffix) - set([""]));
		
	# common portions of environment
	print(f"prefixes: {prefixes}");
	leftcxt = lcs(prefixes);

	print(f"suffixes: {suffixes}");
	rightcxt = lcp(suffixes);

	print(f"/{underlying}/ -> [{surface}] / {leftcxt}_{rightcxt}"); # debug

	# construct genv, g(genv)
	genv = leftcxt + underlying + rightcxt;
	ggenv = leftcxt + surface + rightcxt;
	k = len(genv);
	d = k - len(leftcxt);


	# initialise states
	Q = pref(genv) - {genv};
	sigma = {};
	for qx in Q:
		sigma[qx] = lus(qx, { qx, leftcxt });
	print(Q);

	# form Sigma, Gamma
	Sigma = set();
	for x in fh.values():
		for y in x:
			Sigma.add(y);
	Gamma = T_gf.Gamma;

	# construct edges
	E = set();
	for i in range(0, k): # for each symbol in genv
		q_i = genv[:i]; # from the head of pref_{i}(genv)
		for u in Sigma: # for each possible input on this head...
			v = u; # homomorphic (default)
			q_j = lcp({genv, u}); # go back as little as we can (default)
			if u != genv[i]: # if this symbol does not forward genv...
				if k - d < i: # ... and if we're after the alternate
					v = sigma[q_i] + u; # prepend alternate
			else: # we're met here
				if i == k - 1: # if we're done
					v = ggenv[k - d:]; # output all (delayed + alternated) output
				else: # not yet finished
					q_j = genv[:i+1]; # move forward
			e = (q_i, u, v, q_j);
			E.add(e);

	T_g = FST(Sigma, Gamma);
	T_g.Q = list(Q);
	T_g.E = list(E);
	T_g.qe = "";
	T_g.stout = sigma;

	return T_g, genv, ggenv;

def construct_Tf(genv, ggenv, fh):
	Sigma = set(fh.keys());
	Q = {""};
	sigma = {"": ""};
	E = set();
	for u in Sigma:
		v = fh[u];
		if v == ggenv:
			v = genv;
		E.add(("", u, v, ""));


	T_f = FST(Sigma, set(fh.values()));
	T_f.Q = list(Q);
	T_f.E = list(E);
	T_f.qe = "";
	T_f.stout = sigma;

	return T_f;

""" IDLA
	D: data
	Sigma: Input alphabet
	Gamma: Output alphabet
"""
def idla(D, Sigma, Gamma):
	print("\tLearning from Dataset: ");
	print(D);

	# form T_g(f)
	T_gf = ostia(D, Sigma, Gamma);
	print(f"T_gf Edges:\t{T_gf.E}");
	print(f"T_gf sigma:\t{T_gf.stout}");
	# form f^h
	fh = construct_fh(T_gf);
	print("\tf^h:", fh); # DEBUG

	# form T_g
	T_g, genv, ggenv = construct_Tg(T_gf, fh);

	# form T_f
	T_f = construct_Tf(genv, ggenv, fh);
	print(genv, "->", ggenv);

	return T_f, T_g;
