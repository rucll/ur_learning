from idla import *
from data import flap

t = build_ptt(flap.Data, flap.Sigma, flap.Gamma);
print(t.E);
ot = onward_ptt(t, "", "")[0];
print(ot.E);

T = ostia(flap.Data, flap.Sigma, flap.Gamma);
print(T.E, "\n", T.stout);
