from fst_object import *
from ostia_d import *
from helper import *


# Helper functions

def suff_1(w):
    """Returns 1-suffix of w"""
    if w == "":
        return ""
    else:
        return w[-1]


def get_OS(T,q):
    """Gets output 1-suffixes of state q in FST T"""
    incoming = { tr for tr in T.E if tr[3] == q}
    outs = { tr[2] for tr in incoming}
    suffs = { suff_1(w) for w in outs}
    # print(f"{q}: {suffs}")
    return suffs


def lncat(w,v):
    """Returns wv^-1; i.e. v removed from the end of w"""
    if v == "":
        return w
    elif w.endswith(v):
        return w[0:-len(v)]
    else: 
        print ("using fake lncat")
        return w
        


def si2dla_ex(Dom,D,Rho,Sigma):
    """A less strict version of SI2LDA for dealing with a wider range of data sets"""

    print("Learning from "+str(D)+"\n")

    T_f = ostia_d(Dom,D,Rho,Sigma)

    print("Initial hypothesis for T_f:")
    print("  Q:\t"+str(T_f.Q))
    print("  E:\t"+str(T_f.E))
    print("  q0:\t"+str(T_f.qe))
    print("  stout:\t"+str(T_f.stout)+"\n")

   # get alternation
    alternations = []
    for alphabet in T_f.Sigma:
        outputs = set()
        for tr in T_f.E:
            if tr[1] == alphabet:
                outputs.add(tr[2])
        if len(outputs) > 1:
            alternations.append(alphabet)

    print("alternations", alternations)

    # get states that lead into the alternations
    states_leading = set()
    for var in alternations:
        for tr in T_f.E:
            if tr[1] == var:
                states_leading.add(tr[0])

    print(f"states leading into alternations: {states_leading}")

    # assign q_def to the largest OS
    OS = {}
    for state in states_leading:
        OS[state] = get_OS(T_f, state)
        print(f"State: {OS[state]}")

    largest_os = None
    for key, value in OS.items():
        if len(value) == 0:
            largest_os = key
            # print(f"q_def: {largest_os}" )
            break
        if largest_os == None or len(value) > len(OS[largest_os]):
            largest_os = key
    
    temp_corr = {"qe": [], 'qd': []} 

    for state, value in OS.items():
        if state == largest_os:
            temp_corr["qd"].append(state)

    urs = {}

    for tr in T_f.E:
        morph = tr[1]

        # if the morph alternates, the UR is the one thats in qd
        if morph in alternations:
            if tr[0] in temp_corr['qd']:
                urs[morph] = tr[2]

        else:
            urs[morph] = tr[2]
            
    print(urs)


    
    n_t_f = set()

    for tr in T_f.E:
        if tr[2] != urs[tr[1]] and tr[0] not in temp_corr['qe']:
            temp_corr['qe'].append(tr[0])

        if tr[2] == urs[tr[1]] and tr[0] not in temp_corr["qd"]:
            temp_corr['qd'].append(tr[0])
    
    for state in T_f.Q:
        if state not in temp_corr['qd'] and state not in temp_corr['qe']:
            temp_corr['qd'].append(state)

    both = set(temp_corr['qd']) & set(temp_corr['qe'])

    for state in both:
        temp_corr['qd'].remove(state)


    print('def stuff', temp_corr['qd'])
    print('env stuff', temp_corr['qe'])


    for tr in T_f.E:
        if tr[0] in temp_corr['qd'] and tr[3] in temp_corr["qe"]:
            n_t_f.add(("def", tr[1], tr[2], "env"))
        elif tr[0] in temp_corr['qd'] and tr[3] in temp_corr['qd']:
            print(tr)
            n_t_f.add(("def", tr[1], tr[2], "def"))
        elif tr[0] in temp_corr['qe'] and tr[3] in temp_corr['qe']:
            n_t_f.add(('env', tr[1], tr[2], 'env'))
        elif tr[0] in temp_corr['qe'] and tr[3] in temp_corr['qd']:
            n_t_f.add(('env', tr[1], tr[2], 'def'))
    

    T_f.Q = ["def", "env"]

    T_f.E = list(n_t_f)
    
    print(T_f.Q)

    print(T_f.E)

    q_env = 'env'
    q_def = 'def'

    T_f.stout = {'def': '', 'env': ''}

    Q_g = ["qe","qd"]

    corr = {"qe": q_env, "qd": q_def}
    rroc = {q_env: "qe", q_def: "qd"}

    print("corr:\t\t"+str(corr))

    print("OSs for T_f:\t"+str(OS))

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

                print("w_d for "+s+":\t"+w_d)
                print("w_e for "+s+":\t"+w_e+"\n")

                w_s = lncat(w_e,w_d[1:])

                o_g[("qe",s)] = w_s

                if s != w_s: #This is lns 2-3 from Alg 3
                    tau = s
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

    T_f.E = [ d for d in T_f.E if not d[0]==corr["qe"]]

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
                    w = lncat(w,w_tau)+tau
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
