# An implementation of the IDLA (To Appear)
# Written by Ben Evans

from utility.fst_object import FST
from ostia import *
from helper import *
import types

# prefixes of a string
#     w (str): subject string
#     Returns:
#     	(set): the set of prefixes of the given string.
def pref(w):
	return {w[:j] for j in range(len(w) + 1)};
# suffixes of a string
#     w (str): subject string
#     Returns:
#     	(set): the set of suffixes of the given string.
def suff(w):
	return {w[j:] for j in range(len(w) + 1)};

# supp
def supp(S):
	s = "";
	for sp in S:
		if len(sp) > len(s):
			s = sp;
	return s;

# Longest Common Prefix
# 	S: set of strings
# Returns:
# 	(str): longest common suffix
def lcp(S):
	Sp = set();
	for w in S: # big set of prefixes
		Sp = Sp | pref(w);
	for w in S: # common set of prefixes
		Sp = Sp & pref(w);
	return supp(Sp);

# Longest Common Suffix
#     S: set of strings
#     Returns:
#     	(str): longest common suffix
def lcs(S):
	Sp = set();
	for w in S: # big set of suffixes
		Sp = Sp | suff(w);
	for w in S: # common set of suffixes
		Sp = Sp & suff(w);
	return supp(Sp);


### BEGIN extending FST ###
# Hypothesis Function
def somega(self, e):
	q = str(e[0]);
	v = str(e[2]);
	qp = str(e[3]);
	return v.removeprefix(self.stout[q]) + self.stout[qp];

# Signature of a state
def sig(self, q):
	if q == self.qe:
		return "";
	I = set(); # set of all incoming transitions
	for e in self.E: # of form (r, u, v, q)
		if q != e[3] or q == e[0]:
			continue;
		# we are on a relevant edge
		I.add(sig(self, e[0]) + somega(self, e));
	return lcs(I);

# monkey patching
FST.somega = somega;
FST.sig	= sig;
### END extending FST ###

# form fh
def form_fh(Tgf):
	Tgf.ET = set();
	fh = {};

	# collect terminals
	for e in Tgf.E:
		si = Tgf.sig(e[0]);
		sj = Tgf.sig(e[3]);
		if si != "" and lcs({si, sj}) != si:
			Tgf.ET.add(e);
		else:
			if e[1] not in fh:
				fh[e[1]] = Tgf.somega(e);
	return fh;

# environment function (maximal)
def environment(Tgf, fh):
	# collecting
	prefixes = set();
	varsigma = set();
	vartheta = set();
	for edge in Tgf.ET:
		und = Tgf.stout[edge[0]] + fh[edge[1]];
		sur = edge[2] + Tgf.stout[edge[3]];
		if und != sur: # then is an alternating terminal
			prefix = Tgf.sig(edge[0]).removesuffix(Tgf.stout[edge[0]]);

			prefixes.add(prefix);
			varsigma.add(und);
			vartheta.add(sur);

	# common portions of environment
	print(f"prefixes: {prefixes}");

	pg = lcs(prefixes);
	sg = lcp(varsigma);
	tg = lcp(vartheta);
	print(f"/{sg}/ -> [{tg}] / {pg}_"); # DEBUG

	return pg, sg, tg;

def construct_Tg(p, s, t, Tgf, fh):
	# form Sigma, Gamma
	Sigma = set();
	for x in fh.values():
		for y in x:
			Sigma.add(y);
	Gamma = Tgf.Gamma;
	Tg = FST(Sigma, Gamma);

	# initialise states
	Q = pref(p + s) - { p + s };
	Tg.Q = list(Q);
	Tg.stout = {};
	E = set();
	Tg.qe = "";

	print(Q); # DEBUG
	for q_i in Tg.Q:
		sigma = "";
		if len(q_i) > len(p):
			sigma = q_i.removeprefix(p);
		Tg.stout[q_i] = sigma;
	print(Tg.stout);

	for q_i in Tg.Q:
		# construct edges
		for a in Sigma:
			q_j = q_i + a; # target state
			u = a;
			if q_j not in pref(p + s) - {p + s}: # terminal
				if q_j == p + s: # alternating terminal
					u = t;
				else: # non-alternating
					u = Tg.stout[q_i] + a;
				q_j = lcp({ p + s, a });
				u = u.removesuffix(Tg.stout[q_j]);
			else: # non-terminal (target state exists)
				if Tg.stout[q_j] != "": # are we working on the d-suffix?
					u = ""; # delay output
				else: # identity function
					u = a;
			E.add( (q_i, a, u, q_j) );
	Tg.E = list(E);
	return Tg;

def construct_Tf(p, s, t, fh):
	Sigma = set(fh.keys());
	Q = {""};
	sigma = {"": ""};
	E = set();
	v = p + t;
	kp = len(v); # k'
	for a in Sigma:
		i = kp;
		while i <= len(fh[a]):
			u = fh[a][:i - kp];
			w = fh[a][:i];
			if w.removeprefix(u) == v:
				fh[a] = u + p + s + fh[a][i:];
				i = i + kp;
			else:
				i = i + 1;
		# done
		E.add(("", a, fh[a], ""));


	T_f = FST(Sigma, set(fh.values()));
	T_f.Q = list(Q);
	T_f.E = list(E);
	T_f.qe = "";
	T_f.stout = sigma;

	return T_f;

# IDLA
#     D: data
#     Sigma: Input alphabet
#     Gamma: Output alphabet
def idla(D, Sigma, Gamma):
	print(f"\tLearning from Dataset: {D}");

	# form T_g(f)
	Th = ostia(D, Sigma, Gamma)
	print(f"Th Edges:\t{Th.E}");
	print(f"Th sigma:\t{Th.stout}");

	# form f^h
	fh = form_fh(Th);
	print(f"\tf^h:{fh}"); # DEBUG
	# collate
	p, s, t = environment(Th, fh);
	# construct Tf
	Tf = construct_Tf(p, s, t, fh);
	# construct T_g
	Tg = construct_Tg(p, s, t, Th, fh);

	return Tf, Tg;
