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
    states_leading = []
    for var in alternations:
        for tr in T_f.E:
            if tr[1] == var:
                states_leading.append(tr[0])

    print(f"states leading into alternations: {states_leading}")


    q1 = states_leading[0]
    q2 = states_leading[1]

    # error check in here
    OS = {
        q1: get_OS(T_f, q1),
        q2: get_OS(T_f, q2)
    }


    Q_g = ["qe","qd"]

    corr = {}
    rroc = {}

    if len(OS[q1]) < len(OS[q2]):
        corr["qe"] = q1
        corr["qd"] = q2
        rroc[q1] = "qe"
        rroc[q2] = "qd"
    else:
        corr["qe"] = q2
        corr["qd"] = q1
        rroc[q2] = "qe"
        rroc[q1] = "qd"

    print("corr:\t\t"+str(corr))


    # startandend_count: [# of states that lead out, # of states that lead in]
    # total_count: total number of times a state appears in the list of transitions
    startandend_count = {q: [0, 0] for q in T_f.Q} # [goes out, comes in]
    total_count = {q: 0 for q in T_f.Q}
    for tr in T_f.E:
        startandend_count[tr[0]][0] += 1
        total_count[tr[0]] += 1
        startandend_count[tr[3]][1] += 1
        total_count[tr[3]] += 1

    for q in T_f.Q:
        print(f"{q}: {startandend_count[q]}")
        print(f"{q}: {total_count[q]}")
        if startandend_count[q][0] == 0 or startandend_count[q][1] == 0:
           total_count[q] = -1
           print(q)
        # if startandend_count[q][1] == 0:
        #    total_count[q] = -1
        #    print(q)

   
   
    # assign definition to a state based on # of times it appears
    # q_def = max(total_count, key=total_count.get)

    # assign q_def based on earlier decision b/w alternations
    q_def = corr["qd"]
    print(f"q_def {q_def}")

    # collapse all states that don't have input prefixes or suffixes to definition state
    for idx, tr in enumerate(T_f.E):
        tr = list(tr) # to allow for assignment
        if total_count[tr[0]] == -1:
            print("pp")
            tr[0] = q_def
        if total_count[tr[3]] == -1:
            tr[3] = q_def
        tr = tuple(tr)
        T_f.E[idx] = tr

    
    # add in missing transitions
    for input_alphabet in T_f.Sigma:
        exist_in_state = set()
        for tr in T_f.E:
            if tr[1] == input_alphabet:
                exist_in_state.add(tr[0])
        print(f"Alphabet {input_alphabet}: {exist_in_state}")
        if len(exist_in_state) != 2:
            print(f"Missing: {input_alphabet}")
            output = None
            exists = exist_in_state.pop()

            add_to_state = None
            if exists == corr["qd"]:
                add_to_state = corr["qe"]
            else:
                add_to_state = corr["qd"]

            for tr in T_f.E:
                if tr[1] == input_alphabet:
                    output = tr[2]
                    break
            T_f.E.append((add_to_state, input_alphabet, output, add_to_state))
        
    # e_list = [list(tr) for tr in T_f.E]
    # print(f"e_list: {e_list}")
    # for tr in e_list:
    #     if total_count[tr[0]] == -1:
    #         print("pp")
    #         tr[0] = q_def
    #     if total_count[tr[3]] == -1:
    #         tr[3] = q_def

    # T_f.E = []
    # for tr in e_list:
    #     T_f.E.append(tuple(tr))
        

    print(T_f.E)

    print(T_f.Q)

    # update T_f.Q
    new_Q = set()
    for tr in T_f.E:
        new_Q.add(tr[0])
        new_Q.add(tr[3])
    
    T_f.Q = list(new_Q)

    

    print("OSs for T_f:\t"+str(OS))

    IS = { "qe" : OS[corr["qe"]],
           "qd" : OS[corr["qd"]]
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
    T_g.qe = rroc[q1]
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
            print(r)
            print(rroc)
            # if suff_1(w) not in IS[rroc[r]]:
            #     w = lncat(w,w_tau)+tau
            if r in rroc and rroc[r] in IS:
                if suff_1(w) not in IS[rroc[r]]:
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
