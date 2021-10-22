from si2dla_mod import *
from so2dla import *
from fsi2dla import *

# Zapotec example
# Note: this data comes from a morphological analysis exercise in Chapter 4 of Language Files.
# Data coding: 1 = stick, 2 = dough, 3 = four, 4 = tortilla, 5 = chicken, 6 = rope, A = possessive, B = 3, C = 2

data = [('A','s'),('B','be'),('C','lu'),('1','palu'),('2','kuba'),('3','tapa'),('4','geta'),('5','bere'),('6','do?o'),('A1','spalu'),('A2','skuba'),('A3','stapa'),('A4','sketa'),('A5','spere'),('A6','sto?o'),('AB','spe'),('A1B','spalube'),('A2B','skubabe'),('A3B','stapabe'),('A4B','sketabe'),('A5B','sperebe'),('A6B','sto?obe'),('A1C','spalulu'),('A2C','skubalu'),('A3C','stapalu'),('A4C','sketalu'),('A5C','sperelu'),('A6C','sto?olu')]

morphs = ['A','B','C','1','2','3','4','5','6']
segs = ['p','a','l','u','k','b','t','g','e','r','d','o','?','s']

f,g = si2dla(data,morphs,segs)
























