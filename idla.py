# An implementation of the IDLA (To Appear)
# Written by Ben Evans

from fst_object import FST
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

# wedge
def wedge(S):
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
	return wedge(Sp);

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
	return wedge(Sp);


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
	suffixes = set();
	underlying = None;
	surface = None;
	for edge in Tgf.ET:
		und = Tgf.stout[edge[0]] + fh[edge[1]];
		sur = edge[2] + Tgf.stout[edge[3]];
		if und != sur: # then is an alternating terminal
			prefix = Tgf.sig(edge[0]).removesuffix(Tgf.stout[edge[0]]);
			suffix = lcs({ und, sur });

			prefixes.add(prefix);
			suffixes.add(suffix);

			if underlying or surface is None:
				underlying = und[0];
				surface = sur.removesuffix(suffix);

	# common portions of environment
	print(f"prefixes: {prefixes}");
	print(f"suffixes: {suffixes}");

	leftcxt = lcs(prefixes);
	rightcxt = lcp(suffixes);

	print(f"/{underlying}/ -> [{surface}] / {leftcxt}_{rightcxt}"); # DEBUG

	return leftcxt, underlying, surface, rightcxt;

def construct_Tg(genv, ggenv, p, Tgf, fh):
	# form Sigma, Gamma
	Sigma = set();
	for x in fh.values():
		for y in x:
			Sigma.add(y);
	Gamma = Tgf.Gamma;
	Tg = FST(Sigma, Gamma);

	# initialise states
	Q = pref(genv) - {genv};
	Tg.Q = list(Q);
	Tg.qe = "";
	print(Q); # DEBUG

	Tg.stout = {};
	for qx in Q: # and state output
		# TODO: I'm sure there's a better way to do this...
		sigma = "";
		if p in pref(qx):
			sigma = qx.removeprefix(p);
		Tg.stout[qx] = sigma;
		print(f"sigma[{qx}] = {sigma}"); # DEBUG

	# construct edges
	E = set();
	for q_i in Tg.Q:
		for u in Sigma:
			q_j = q_i + u; # target state
			if q_j not in pref(genv) - {genv}: # terminal
				if q_j == genv: # alternating terminal
					v = ggenv.removeprefix(p);
				else: # non-alternating
					v = Tg.stout[q_i] + u;
				q_j = lcp({genv, u});
			else: # non-terminal (target state exists)
				if Tg.stout[q_j] != "": # are we working on the d-suffix?
					v = ""; # delay output
				else: # identity function
					v = u;
			E.add( (q_i, u, v, q_j) );
	Tg.E = list(E);
	return Tg;

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

# IDLA
#     D: data
#     Sigma: Input alphabet
#     Gamma: Output alphabet
def idla(D, Sigma, Gamma):
	print(f"\tLearning from Dataset: {D}");

	# form T_g(f)
	Tgf = ostia(D, Sigma, Gamma)
	print(f"Tgf Edges:\t{Tgf.E}");
	print(f"Tgf sigma:\t{Tgf.stout}");

	# form f^h
	fh = form_fh(Tgf);
	print(f"\tf^h:{fh}"); # DEBUG
	# collate
	leftcxt, underlying, surface, rightcxt = environment(Tgf, fh);
	# construct genv, g(genv)
	genv = leftcxt + underlying + rightcxt;
	ggenv = leftcxt + surface + rightcxt;
	# construct Tf
	Tf = construct_Tf(genv, ggenv, fh);
	# construct T_g
	Tg = construct_Tg(genv, ggenv, leftcxt, Tgf, fh);

	return Tf, Tg;
