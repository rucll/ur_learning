# SI2DLA Walkthrough
## Introductory notes

This guide explains the decomposition part of SI2DLA using the toy example from Hua & Jardine (2021). 

The morphemes from this example are:
    
    1 → tat
    2 → ada
    3 → d

The phonological rule is:
```d → t / t_ ```. In words, d becomes t after t.


Here are some examples of the morphophonological process taking place.
    
    13 → tatd → tatt
    23 → adad → adad


The <b>learner only gets to see the final surface mappings</b>, such as:
    
    1 → tat
    2 → ada
    3 → d 
    13 → tatt 
    23 → adad 
    113 → tattatt

The goal of SI2DLA is to recover two separate transducers: 

<b> T_f </b>: (morphemes to underlying forms)
    
    1 → tat
    2 → ada 
    3 → d

<b>T_g</b>: (underlying forms to surface forms)
    
    representing d → t after t



## OSTIA

SI2DLA begins by calling OSTIA: 
```python
T_f = ostia(D, Rho, Sigma)
```

OSTIA learns one composed transducer. This transducer maps morpheme strings directly to surface strings. 

For this example, assume OSTIA 
learns the following two-state 
machine: 
    
    State q1:
        1 : tat  → q2
        2 : ada  → q1
        3 : d    → q1

    State q2: 
        1 : tat  → q2
        2 : ada  → q1 
        3 : t    → q2 
        
Essentially,

**q1** means: the previous output does not end in t
 
**q2** means: the previous output ends in t 

As you can see, the difference between q1 and q2 is only visible on morpheme 3, since from q1, 3 outputs d, while from q2, 3 outputs t.

## Output Suffixes

The code computes OS: 

```python
OS = { 
    q2 : get_OS(T_f,q2) | {""}, 
    q2 : get_OS(T_f,q2) 
} 
```

OS means the set of final output 
symbols on transitions entering 
each state, also known as the 
output suffixes. 

*Note: the helper function suff_1(w) 
returns the last symbol of w.*

Examples: 
 
    suff_1("tat") = "t" 
    suff_1("ada") = "a" 
    suff_1("d")   = "d" 
    suff_1("t")   = "t" 
Now the OS is computed manually. 

**For q1:**

Incoming transitions to q1: 
 
    q1 → 2:ada → q1 
    q1 → 3:d → q1 
    q2 → 2:ada → q1 
 
Outputs: 
 
    ada 
    d 
    ada 
 
Final symbols: 
 
    a 
    d 
    a

So: 
 
    OS(q1) = {a, d} 
 
Since q1 is the initial state, the code adds the empty string: 
 
    OS(q1) = {"", a, d} 

**For q2:**

Incoming transitions to q2: 
 
    q1 → 1:tat → q2 
    q2 → 1:tat → q2 
    q2 → 3:t → q2 
 
Outputs: 
 
    tat 
    tat 
    t 
 
Final symbols: 
 
    t 
    t 
    t 
 
So: 
 
    OS(q2) = {t} 

**Therefore:**
```
OS = { 
    q1 : {"", a, d}, 
    q2 : {t} 
} 
```
This is the first key decomposition clue.

The state q2 is reached exactly when the previous output ends in t. 

That means q2 is encoding the environment for the rule d → t after t.

## Choosing the Default/Environment State

The code now chooses which OSTIA state corresponds to the environment state.

It compares the sizes of the OS sets: 

    OS(q1) = {"", a, d} 
    size = 3 
    
    OS(q2) = {t} 
    size = 1 

The state with fewer possible 
incoming suffixes is treated as 
the environment state. 

So:  q2 becomes qe + q1 becomes qd

In the code: 
```python
corr = { 
    "qe" : q2, 
    "qd" : q1 
} 
```
and the reverse map is: 
```python
rroc = { 
    q2 : "qe", 
    q1 : "qd" 
}
```

The names mean: 
<dl>
<dt> qe: </dt>
    <dd>environment state </dd>
 
<dt> qd: </dt>
    <dd>default or definition state </dd>
</dl>

*Why does this make sense?*

Because the environment for this rule is very specific: **after t**

So the state associated only with the suffix t is the environment state.


## Computing IS

The code now constructs IS: 
```python
IS = { 
    "qe" : OS[corr["qe"]], 
    "qd" : OS[corr["qd"]] 
} 
```
Substituting the values: 
    
    corr["qe"] = q2 
    corr["qd"] = q1 
So: 

    IS("qe") = OS(q2) = {t} 
    
    IS("qd") = OS(q1) = {"", a, d} 

Therefore: 
```python
IS = { 
    "qe" : {t}, 
    "qd" : {"", a, d} 
}
```

IS tells T_g which suffixes correspond to which state. 

In plain English: 
<dl>
<dt> If the previous output suffix is t: </dt>
    <dd>go to qe </dd>
<dt>If the previous output suffix is empty, a, or d: </dt>
    <dd>go to qd </dd>
</dl>
This gives T_g the memory it needs.

## Building d_g (Transition Function) 
The code builds d_g like this: 
```python
d_g = {} 
 
for q in Q_g: 
    for s in Sigma: 
        for r in Q_g: 
            if s in IS[r]: 
                d_g[(q,s)] = r 
```
Here, ```Q_g = ["qe", "qd"] ```
and the output alphabet is: 
```Sigma = {a, d, t} ```

The transition function d_g says: 

>*If T_g reads symbol s, which state should it go to?*


Since ```IS("qe") = {t}``` and ```IS("qd") = {"", a, d} ```, we get: 

- reading t sends the machine to qe 
- reading a sends the machine to qd 
- reading d sends the machine to qd 

So the full transition function is: 
```
d_g[("qe", "t")] = "qe" 
d_g[("qd", "t")] = "qe" 
 
d_g[("qe", "a")] = "qd" 
d_g[("qd", "a")] = "qd" 
 
d_g[("qe", "d")] = "qd" 
d_g[("qd", "d")] = "qd" 
```
Notice that the current state does not really matter here, since this is a strictly local environment.


## Building o_g (Output Function) 

Now the algorithm needs to decide what T_g outputs. 

The code loops through each output symbol s in Sigma: 
```python
for s in Sigma: 
    o_g[("qd",s)] = s 
```
This means:

In the default state qd, output every symbol as is. 

So: 
```
o_g[("qd","a")] = "a" 
o_g[("qd","d")] = "d" 
o_g[("qd","t")] = "t" 
```
 
Now the algorithm computes what happens in qe. 

For each symbol s, it compares: 
- w_d: the output from the default state qd 
- w_e: the output from the environment state qe 

The code finds ```d_tr = transition from corr["qd"] whose output begins with s ```

Since corr["qd"] = q1, this means: 
>*look at a transition from q1*

Then ```w_d = output of that q1 transition ```

Then it finds the corresponding transition from qe with the same input: ```w_e = output from q2 on that same input ```

*Finally:* ```w_s = lncat(w_e, w_d[1:]) ```and sets: ```o_g[("qe",s)] = w_s ```

This is where the decomposition is taking place. The next section will make more clear what is taking place. 

## Computing o_g for Each Symbol 

We now compute this manually. 

Recall the composed OSTIA machine: 
```
q1: 
    1 : tat 
    2 : ada 
    3 : d 
q2: 
    1 : tat 
    2 : ada 
    3 : t 
```

### *Case 1: s = a*

We need a transition from q1 whose output begins with a. 

From q1, 
```2 : ada```

So: 
```d_tr = q1 → 2:ada → q1```,
```w_d = "ada"```

Now find the q2 transition with the same input, namely input 2: 
```q2 → 2:ada → q1 ```

So: 
```w_e = "ada" ```

Now compute: 
```w_d[1:] = "da" ```

Then: 
```w_s = lncat(w_e, w_d[1:]) ```

That is: 
```w_s = lncat("ada", "da") ```

The function lncat(w,v) removes v from the end of w. 

Since "ada" ends in "da": 
```lncat("ada", "da") = "a" ```

Therefore: 
```o_g[("qe","a")] = "a" ```

So in the environment state: 
***a stays a***

### *Case 2: s = d*

We need a transition from q1 whose output begins with d. 

From q1, 
```3 : d ```

So: 
```d_tr = q1 → 3:d → q1 ```, 
```w_d = "d" ```

Now find the q2 transition with the same input, namely input 3: 
```q2 → 3:t → q2 ```

So: 
```w_e = "t"```

Now compute: 
```w_d[1:] = "" ```

Then: 
```w_s = lncat(w_e, "") ```

Since removing the empty string changes nothing: 
```lncat("t", "") = "t" ```

Therefore: 
```o_g[("qe","d")] = "t" ```

This is the crucial output. 

In the environment state: 
***d becomes t***

This recovers the phonological rule. 

### *Case 3: s = t*

We need a transition from q1 whose output begins with t. 

From q1, ```1 : tat ```

So: 
```d_tr = q1 → 1:tat → q2 ```,
```w_d = "tat" ```

Now find the q2 transition with the same input, namely input 1: ```q2 → 1:tat → q2 ```

So: ```w_e = "tat" ```

Now compute: ```w_d[1:] = "at" ```

Then: 
```w_s = lncat(w_e, w_d[1:]) ```

That is: 
```w_s = lncat("tat", "at") ```

Since "tat" ends in "at": 
```lncat("tat", "at") = "t" ```

Therefore: 
```o_g[("qe","t")] = "t" ```

So in the environment state: ***t stays t***

## Putting T_g Together 

Now we combine d_g and o_g. 

Recall that: 

```
d_g[("qe", "t")] = "qe" 
d_g[("qd", "t")] = "qe"

d_g[("qe", "a")] = "qd" 
d_g[("qd", "a")] = "qd" 

d_g[("qe", "d")] = "qd" 
d_g[("qd", "d")] = "qd" 
```

and 

```
o_g[("qd","a")] = "a" 
o_g[("qd","d")] = "d" 
o_g[("qd","t")] = "t" 

o_g[("qe","a")] = "a" 
o_g[("qe","d")] = "t" 
o_g[("qe","t")] = "t" 
```

Putting this information together, T_g has two states, qd and qe. 

**In qd:**
```
a : a  → qd 
d : d  → qd 
t : t  → qe 
```
**In qe:**
```
a : a  → qd 
d : t  → qe 
t : t  → qe 
```
This is exactly the phonological rule machine. 

The important transition is: 
**```qe → d:t → qe ```**

This means if the previous output was t, then reading d outputs t. 

That is:  **```d → t / t _ ```**

## Deciding on tau and w_tau 

In the code: 
``` python
if s != w_s: 
    tau = s 
    w_tau = w_s 
```
This detects the symbol that changes in the environment. 
From our calculations: 
<dl>
<dt>for s = a: </dt>
    <dd>w_s = a 
    <dd>no change 
 
<dt>for s = d: </dt>
    <dd>w_s = t 
    <dd>change 
 
<dt>for s = t: </dt>
    <dd>w_s = t 
    <dd>no change 

</dl>

So **```tau = d ```** and  **```w_tau = t ```**

This means the underlying symbol d becomes t in the environment. 

*The algorithm has now identified the alternation.*


## Modifying T_f 

So far, we have built T_g. 

Now the algorithm modifies the original OSTIA transducer in order to recover T_f.

Recall that the OSTIA machine was: 
```
q1: 
    1 : tat  → q2 
    2 : ada  → q1 
    3 : d    → q1 
 
q2: 
    1 : tat  → q2 
    2 : ada  → q1 
    3 : t    → q2 
```
Since qe = q2, the code deletes 
every transition leaving q2: 
```python
T_f.E = [ 
    d for d in T_f.E 
    if not d[0] == corr["qe"] 
] 
```
Because ```corr["qe"] = q2 ``` we delete: 
```
q2 → 1:tat → q2 
q2 → 2:ada → q1 
q2 → 3:t → q2 
```
The remaining transitions are: 
```
q1 → 1:tat → q2 
q1 → 2:ada → q1 
q1 → 3:d → q1 
```

At this point, T_f only keeps the default-state transitions. 
This makes sense because q1 is the state where the forms are not affected by the phonological environment. 



## Opacity 

Next the code checks whether any remaining transition still points to the wrong kind of state. 

The relevant code is: 
```python
new_E = [] 
 
for (q,rho,w,r) in T_f.E: 
    if q == corr["qd"]: 
        if suff_1(w) not in 
IS[rroc[r]]: 
            w = 
lncat(w,w_tau)+tau 
    new_E.append((q,rho,w,q)) 
```
Since: 
```corr["qd"] = q1 ```
the code examines all transitions leaving q1. 

These are: 
```
q1 → 1:tat → q2 
q1 → 2:ada → q1 
q1 → 3:d → q1 
```
The code asks: 
>*Does the output suffix of this transition match the state it originally entered?*

If not, then the output has been distorted by the phonology and needs to be repaired.

### *Transition 1:*
```
q1 → 1:tat → q2 
```
Here, ```w = "tat"``` and ```r = q2```

The final symbol is ```suff_1("tat") = t ```

Now, ```rroc[q2] = "qe" ```and ```IS("qe") = {t} ```

Since ```t is in {t}```, there is no problem. 
So the output stays: 
>**tat** 

### *Transition 2:*
```
q1 → 2:ada → q1 
```
Here, ```w = "ada" ``` and ```r = q1 ```

The final symbol is: ```suff_1("ada") = a```

Now, ```rroc[q1] = "qd" ``` and ```IS("qd") = {"", a, d} ```

Since ```a is in {"", a, d} ```, there is no problem. So the output stays: 
>**ada**

### *Transition 3:*
```
q1 → 3:d → q1 
```
Here, ```w = "d" ```and ```r = q1```

The final symbol is: ```suff_1("d") = d ```

Now, ```rroc[q1] = "qd" ```and ```IS("qd") = {"", a, d} ```

Since ```d is in {"", a, d} ```, there is no problem. So the output stays: 
> **d**

In this particular example, no opacity adjustment is needed.

However, if opacity adjustment was necessary, the code ```w = lncat(w,w_tau) + tau ```replaces the alternate surface form of the suffix with the true underlying form of the suffix.

## Finishing T_f 

Finally, the code forces all remaining transitions to loop back to the single remaining state. 

The line 
```new_E.append((q,rho,w,q)) ```
means: 
* keep the same start state, 
* keep the same input, 
* keep the repaired output, 
* but make the transition return to q. 

So: 

```q1 → 1:tat → q2``` becomes ```q1 → 1:tat → q1 ```

```q1 → 2:ada → q1``` stays ```q1 → 2:ada → q1 ```

```q1 → 3:d → q1``` stays ```q1 → 3:d → q1```

Then the code sets: 
```T_f.Q = [corr["qd"]] ```

Since ```corr["qd"] = q1 ``` we get ```T_f.Q = [q1] ```

So the final T_f is one-state: 
```
q1: 
    1 : tat  → q1 
    2 : ada  → q1 
    3 : d    → q1 
```
This is exactly the morphology function: 
```
1 → tat 
2 → ada 
3 → d 
```



## The Final Decomposed Machines 

The original OSTIA machine was one composed transducer: 
```
q1: 
    1 : tat  → q2 
    2 : ada  → q1 
    3 : d    → q1 
 
q2: 
    1 : tat  → q2 
    2 : ada  → q1 
    3 : t    → q2 
```

SI2DLA decomposes it into two 
machines. 

First machine, **T_f:**
```
q1: 
    1 : tat  → q1 
    2 : ada  → q1 
    3 : d    → q1 
```
This is the morphology-to-underlying-form transducer. 

Second machine, **T_g:** 
```
qd: 
    a : a  → qd 
    d : d  → qd 
    t : t  → qe 
 
qe: 
    a : a  → qd 
    d : t  → qe 
    t : t  → qe 
```
This is the phonology transducer.
