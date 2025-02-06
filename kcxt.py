# categorise PBase by k-contexts
import csv, sys

# cxt   3 2 1 0 _ 0 1 2 3
# k     _ 2 3 4 5 6 7 8 9
kcxt = [0,0,0,0,0,0,0,0,0]; # max size is 9

t = 0;
with open(sys.argv[1], newline='') as c:
    cread = csv.reader(c, delimiter='\t');
    next(c); # skip header
    for line in cread:
        context = [line[i] for i in range(11, 19)];
        k = len(list(filter(None, context))); # implicit + 1 for the alternate
        kcxt[k] += 1;
        t += 1;

def per(j):
    p = 0.0;
    for i in j:
        p += (kcxt[i] / t) * 100;

    return format(p, '.2f');

for i in range(0, 8):
    p = per([i]);
    pl = per([j for j in range(0, i)] + [i]);
    print(f"{kcxt[i]}/{t} ({p}%) \t\tk = {i+1}\t{pl}% k <= {i + 1}");
