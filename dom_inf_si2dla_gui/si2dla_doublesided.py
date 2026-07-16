"""
SI2DLA for double sided contexts
"""
from utility.fst_object import *
from ostia import *
from utility.helper import *


# Helper functions

def suff_1(w):
    """Returns 1-suffix of w"""
    if w == "":
        return ""
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

def lncat(w,v):
    """Returns wv^-1; i.e. v removed from the end of w"""
    if v == "":
        return w
    elif w.endswith(v):
        return w[0:-len(v)]
    

def lncat_format(w, v):
    
    # print(f"LNCAT: {w}, {v}")
    if len(v) == 0:
        return w

    elif w[-len(v): ] == v:
        return w[0:-len(v)]
    
    else: 
        print ("Does not end with")
        return w
        



# Main algorithm

def si2dla(D,Rho,Sigma):
    """Implements SI2LDA from Hua & Jardine 2021"""

    print("Learning from "+str(D)+"\n")

    T_f = ostia(D,Rho,Sigma)

    print("Initial hypothesis for T_f:")
    print("  Q:\t"+str(T_f.Q))  # n: set of states
    print("  E:\t"+str(T_f.E))  # n: set of edges (starting state, input char, output string, ending state)
    print("  q0:\t"+str(T_f.qe))    # n: initial state
    print("  stout:\t"+str(T_f.stout)+"\n") # n: state outputs (state, output)
    
    
    

    q1 = T_f.Q[0]   # n: state 1
    q2 = T_f.Q[1]   # n: state 2
    q3 = T_f.Q[2]   # n: state 3

    OS = { q1 : get_OS(T_f,q1) | {""},  # n: list of incoming output strings' suffixes per state
           q2 : get_OS(T_f,q2),
           q3 : get_OS(T_f, q3)
    }

    #*** construct_T_g

    Q_g = ["qe","qd", 'qt']

    corr = {}
    rroc = {}

    remaining_states = [q1, q2, q3]

    if len(T_f.stout[q1]) > 0:
        corr['qt'] = q1
        rroc[q1] = 'qt' 
        remaining_states.remove(q1)

    elif len(T_f.stout[q2]) > 0:
        corr['qt'] = q2
        rroc[q2] = 'qt' 
        remaining_states.remove(q2)

    elif len(T_f.stout[q3])> 0:
        corr['qt'] = q3
        rroc[q3] = 'qt'
        remaining_states.remove(q3)

    if len(OS[remaining_states[0]]) > len(OS[remaining_states[1]]):
        corr['qd'] = remaining_states[0]
        corr['qe'] = remaining_states[1]
        rroc[remaining_states[0]] = 'qd'
        rroc[remaining_states[1]] = 'qe'
    else:
        corr['qd'] = remaining_states[1]
        corr['qe'] = remaining_states[0]
        rroc[remaining_states[1]] = 'qd'
        rroc[remaining_states[0]] = 'qe'

    OS[corr['qe']] = {T_f.stout[corr['qt']][0]}

    print("OSs for T_f:\t"+str(OS))

    

    print("corr:\t\t"+str(corr))


    IS = {
        "qt": OS[corr['qt']],
        'qe': OS[corr['qe']],
        'qd': OS[corr['qd']]
    }


    print("ISs for T_g:\t"+str(IS)+"\n")


    d_g = {}

    for q in Q_g:
        if q != 'qt':
            for s in Sigma:
                if s in IS['qt']:
                    d_g[(q, s)] = 'qt'
                if s in IS['qe']:
                    d_g[(q,s)] = 'qe'
                if s in IS['qd']:
                    d_g[(q,s)] = 'qd'
    
    for s in Sigma:
        if s in IS['qe']:
            d_g[('qt', s)] = 'qe'
        elif s in IS['qt']:
            d_g[('qt', s)] = 'qt'
        elif s in IS['qd']:
            d_g[('qt', s)] = 'qd'
        
    
    
    print("d_g:\t"+str(d_g)+"\n")


    o_g = {}

    for s in Sigma:
        o_g[('qd', s)] = s

        d_trs = [tr for tr in T_f.E if tr[0] == corr['qd'] and tr[2][0] == s]

        #gather all alternations
        for d in d_trs:

            print(f'Alternation 1: {d[2]}')

            env_tr = [tr for tr in T_f.E if tr[0] == corr['qe'] and tr[1] == d[1]]

            env_tr = env_tr[0]

            print(f'Alternation 2: {env_tr[2]}')


            trg_tr = [tr for tr in T_f.E if tr[0] == corr['qt'] and tr[1] == d[1] and tr[3] == env_tr[3]]

            trg_tr = trg_tr[0]

            print(f"Alternation 3: {trg_tr[2]}")


            # handle alternations coming from env state
            w_d = d[2]
            w_e = env_tr[2]
            w_s = lncat_format(w_e, w_d[1:])
            
            # if the initial phoneme changes, then it means this phoneme must wait until it sees the right context
            if w_s != tuple(s) and w_s != ():
                o_g[('qt', s)] = 'lambda'

            else:
                o_g[('qt', s)] = w_s

            # handle alternations coming from target state
            w_e = trg_tr[2]

            # if the SR has the same length as initial UR, then deletion
            if len(w_e) == len(w_d):
                w_s = ''
            
            else:
                # all alternations from target state have extra phonemes
                w_s = w_e[0] + s

            

            o_g[('qe', s)] = w_s

        
        if not d_trs:
            o_g[('qe', s)] = ''.join(T_f.stout[corr['qt']]) + s
            o_g[('qt', s)] = s


    E_g = []

    for (q,s) in d_g.keys():
        E_g.append((q,s,o_g[(q,s)],d_g[(q,s)]))
            

    T_g = FST(Rho,Sigma)
    T_g.Q = Q_g
    T_g.E = E_g
    # T_g.qe = rroc[q_def]
    T_g.stout = { "qe" : T_f.stout[corr["qt"]], "qd" : T_f.stout[corr["qd"]], 'qt': T_f.stout[corr['qe']] }

    print("Hypothesis for T_g:")
    print("  Q:\t"+str(T_g.Q))
    print("  E:\t"+str(T_g.E))
    print("  q0:\t"+str(T_g.qe))
    print("  stout:\t"+str(T_g.stout)+"\n")


    # construct UR fst
    mod_e = []

    T_f.Sigma = Rho

    for tr in T_f.E:
        if tr[0] == corr['qd']:
            if tr[3] == corr['qt']:
                upd_tr = (tr[0], tr[1], tr[2] + T_f.stout[corr['qt']], tr[3])
                mod_e.append(upd_tr)
            else:
                mod_e.append(tr)
    
    T_f.E = mod_e

    print("E_f after deletions: "+str(T_f.E)+"\n")

    return T_f, T_g


    #*** modify_T_f

    # T_f.E = [ d for d in T_f.E if not d[0]==corr["qe"]]

    # print("E_f after deletions: "+str(T_f.E)+"\n")

    # new_E = []

    # for (q,rho,w,r) in T_f.E:
    #     if q == corr["qd"]:
    #         if suff_1(w) not in IS[rroc[r]]:
    #             w = lncat(w,w_tau)+tau
    #     new_E.append((q,rho,w,q)) #Step 1 of merging is here too

    # T_f.E = new_E

    # print("E_f after opacity adjustment: "+str(T_f.E)+"\n")

    # print("Merging...\n")

    # T_f.Q = [corr["qd"]]
    # T_f.qe = corr["qd"]
    # T_f.stout = {corr["qd"]:T_f.stout[corr["qe"]]}

    # print("Final hypothesis for T_f:")
    # print("  Q:\t"+str(T_f.Q))
    # print("  E:\t"+str(T_f.E))
    # print("  q0:\t"+str(T_f.qe))
    # print("  stout:\t"+str(T_f.stout)+"\n")

    # return (T_f,T_g) 
