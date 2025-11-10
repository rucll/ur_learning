import sys
sys.path.append('..')
from utility.fst_object import *
from ostia_d import *
from utility.helper import *


# Helper functions

def suff_1(w):
    """Returns 1-suffix of w"""
    if w == ():
        return ''
    else:
        return w[-1]


def get_OS(T,q):
    """Gets output 1-suffixes of state q in FST T"""
    # print(tuple(T.E[1]))
    incoming = { tuple(tr) for tr in T.E if tr[3] == q}
    outs = { tr[2] for tr in incoming}
    suffs = { suff_1(w) for w in outs}
    # print(f"{q}: {suffs}")
    return suffs

# lncat function handling tuples/list (the original function can be deleted later)
def lncat_format(w, v):
    
    # print(f"LNCAT: {w}, {v}")
    if len(v) == 0:
        return w

    elif w[-len(v): ] == v:
        return w[0:-len(v)]
    
    else: 
        print ("using fake lncat")
        return w


def lncat(w,v):
    """Returns wv^-1; i.e. v removed from the end of w"""
    if v == "":
        return w
    elif str(w).endswith(str(v)):
        return w[0:-len(v)]
    else: 
        print ("using fake lncat")
        return w
        


def si2dla_ex(Dom,D,Rho,Sigma):
    """A less strict version of SI2LDA for dealing with a wider range of data sets"""

    print("Learning from "+str(D)+"\n")

    T_f = ostia_d(Dom,D,Rho,Sigma)
    

    print("Initial hypothesis for OSTIA D T_f:")
    print("  Sigma:\t"+str(T_f.Sigma))
    print("  Q:\t"+str(T_f.Q))
    print("  E:\t"+str(T_f.E))
    print("  q0:\t"+str(T_f.qe))
    print("  stout:\t"+str(T_f.stout)+"\n")


   # get which morphemes alternate by checking number of different SRs
    alternations = []
    for alphabet in T_f.Sigma:
        outputs = set()
        for tr in T_f.E:
            if tr[1] == alphabet:
                outputs.add(tr[2])
        if len(outputs) > 1:
            alternations.append(alphabet)

    # get states that lead into the alternations
    states_leading = set()
    for var in alternations:
        for tr in T_f.E:
            if tr[1] == var:
                states_leading.add(tr[0])


    # gather OSes of each state that leads into alternation
    OS = {}
    for state in states_leading:
        OS[state] = get_OS(T_f, state)

    # assign q_def to the largest OS or if the state is lambda in states_leading
    largest_os = None
    for key, value in OS.items():
        if len(value) == 0:
            largest_os = key
            # print(f"q_def: {largest_os}" )
            break
        if largest_os == None or len(value) > len(OS[largest_os]):
            largest_os = key
    
    temp_corr = {"qe": [], "qd": []} 

    for state, value in OS.items():
        if state == largest_os:
            temp_corr["qd"].append(state)

    # store initial UR hypothesis
    urs = {}

    for tr in T_f.E:
        morph = tr[1]
        # if the morpheme alternates, the UR is the one thats in q_def
        if morph in alternations:
            if tr[0] in temp_corr['qd']:
                urs[morph] = tr[2]      
        else:
            urs[morph] = tr[2]
    
    n_t_f = set()

    # mark each transition in ostia-d T_f as either q_def or q_env
    for tr in T_f.E:
        # if a UR has not been stored yet, store it
        if tr[1] not in urs:
            urs[tr[1]] = tr[2]


        # if the morpheme's SR doesn't match the UR, mark the state q_env
        if tr[2] != urs[tr[1]] and tr[0] not in temp_corr['qe']:
            temp_corr['qe'].append(tr[0])

        # if the morpheme's SR matches the UR, mark the state q_def
        if tr[2] == urs[tr[1]] and tr[0] not in temp_corr["qd"]:
            temp_corr['qd'].append(tr[0])
    
    # for any state not labelled, mark them q_def
    for state in T_f.Q:
        if state not in temp_corr['qd'] and state not in temp_corr['qe']:
            temp_corr['qd'].append(state)

    # remove any overlapping states from q_def
    both = set(temp_corr['qd']) & set(temp_corr['qe'])

    for state in both:
        temp_corr['qd'].remove(state)



    # construct 2 state T_f using state correspondences in temp_corr
    for tr in T_f.E:
        if tr[0] in temp_corr['qd'] and tr[3] in temp_corr["qe"]:
            n_t_f.add(("def", tr[1], tr[2], "env"))
        elif tr[0] in temp_corr['qd'] and tr[3] in temp_corr['qd']:
            # print(tr)
            n_t_f.add(("def", tr[1], tr[2], "def"))
        elif tr[0] in temp_corr['qe'] and tr[3] in temp_corr['qe']:
            n_t_f.add(('env', tr[1], tr[2], 'env'))
        elif tr[0] in temp_corr['qe'] and tr[3] in temp_corr['qd']:
            n_t_f.add(('env', tr[1], tr[2], 'def'))        

    T_f.Q = ["def", "env"]
    T_f.qe = 'def'
    T_f.E = list(n_t_f)
    T_f.stout = {'def': '', 'env': ''}

    print("Initial hypothesis for 2 state T_f:")
    print("  Sigma:\t"+str(T_f.Sigma))
    print("  Q:\t"+str(T_f.Q))
    print("  E:\t"+str(T_f.E))
    print("  q0:\t"+str(T_f.qe))
    print("  stout:\t"+str(T_f.stout)+"\n")
    
    q_env = 'env'
    q_def = 'def'


    Q_g = ["qe","qd"]

    corr = {"qe": q_env, "qd": q_def}
    rroc = {q_env: "qe", q_def: "qd"}

    # print("corr:\t\t"+str(corr))

    # print("OSs for T_f:\t"+str(OS))

    # IS = { "qe" : OS[corr["qe"]],
    #        "qd" : OS[corr["qd"]]
    # }\
    
    IS =  {
        "qe": get_OS(T_f, corr["qe"]),
        "qd": get_OS(T_f, corr["qd"])
    }

    if len(IS["qe"]) > 1:
        IS["qe"] = IS["qe"] - (IS["qe"] & IS["qd"])
    IS["qd"] = IS["qd"] - (IS["qe"] & IS["qd"])

    print("ISs for T_g:\t"+str(IS)+"\n")

    d_g = {}

    for q in Q_g:
        for s in Sigma:
            if s in IS["qe"]:
                d_g[(q,s)] = "qe"
            else:
                d_g[(q,s)] = "qd"
            # for r in Q_g:
            #     if s in IS[r]:
            #         d_g[(q,s)] = r

    # print("d_g:\t"+str(d_g))

    o_g = {}

    for s in Sigma:
        o_g[("qd",s)] = s

        # New here: look for *each* transition whose output starts with s, and see if there is a matching
        # transition from corr[qe]. This allows us to calculate s with a single transition from corr[qe],
        # instead of necessarily needing *every* transition from corr[qd] paired with one from corr[qe].
        d_trs = [ tr for tr in T_f.E if tr[0] == corr["qd"] and tr[2][0] == s ]

        found = False

        for t in d_trs:
            w_trs = [ tr for tr in T_f.E if tr[0] == corr["qe"] and tr[1] == t[1]]

            if w_trs != []:

                found = True

                w_d = t[2]

                w_e = w_trs[0][2]

                print("w_d for "+str(s)+":\t"+str(w_d))
                print("w_e for "+str(s)+":\t"+str(w_e)+"\n")

                w_s = lncat_format(w_e,w_d[1:])

                if w_s == ():
                    w_s = ('',)

                o_g[("qe",s)] = ''.join(w_s)

                if tuple(s) != w_s: #This is lns 2-3 from Alg 3
                    tau = tuple(s)
                    w_tau = w_s

        if found == False:
            o_g[("qe",s)] = s


    # Translate transitions into fst_object FST format
    E_g = []

    for (q,s) in d_g.keys():
        E_g.append((q,s,o_g[(q,s)],d_g[(q,s)]))

    # print("E_g:\t"+str(E_g))

    T_g = FST(Rho,Sigma)
    T_g.Q = Q_g
    T_g.E = E_g
    T_g.qe = rroc[q_def]
    T_g.stout = { "qe" : T_f.stout[corr["qe"]], "qd" : T_f.stout[corr["qd"]] }

    print("Hypothesis for T_g:")
    print("  Q:\t"+str(T_g.Q))
    print("  E:\t"+str(T_g.E))
    print("  q0:\t"+str(T_g.qe))
    print("  stout:\t"+str(T_g.stout)+"\n")


    #*** modify_T_f    
    mod_e = []
    T_f.Sigma = set()

    # T_f.E = [ d for d in T_f.E if not d[0]==corr["qe"]]
    for tr in T_f.E:
        if tr[0] != corr['qe']:
            mod_e.append(tr)
            T_f.Sigma.add(tr[1])

    T_f.E = mod_e

    # add in missing URs
    for morph, ur in urs.items():
        if morph not in T_f.Sigma:
            T_f.E.append(("def", morph, ur, "def"))
    

    print("E_f after deletions: "+str(T_f.E)+"\n")

    new_E = []

    for (q,rho,w,r) in T_f.E:
        if q == corr["qd"]:
            # print(r)
            # print(rroc)
            # if suff_1(w) not in IS[rroc[r]]:
            #     w = lncat(w,w_tau)+tau
            if r in rroc and rroc[r] in IS:
                if suff_1(w) not in IS[rroc[r]]:
                    print("opaque: ", rho)
                    print(w_tau)
                    print(tau)
                    w = lncat_format(w,w_tau)+tau # tau -> w_tau / env _
        new_E.append((q,rho,w,q)) #Step 1 of merging is here too

    T_f.E = new_E

    print("E_f after opacity adjustment: "+str(T_f.E)+"\n")

    print("Merging...\n")

    T_f.Q = [corr["qd"]]
    T_f.qe = corr["qd"]
    T_f.stout = {corr["qd"]:T_f.stout[corr["qe"]]}

    print("Final hypothesis for T_f:")
    print("  Q:\t"+str(T_f.Q))
    print("  E:\t"+str(T_f.E))
    print("  q0:\t"+str(T_f.qe))
    print("  stout:\t"+str(T_f.stout)+"\n")

    return (T_f,T_g)
