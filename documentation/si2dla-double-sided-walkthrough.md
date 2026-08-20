# SI2DLA Double-Sided Walkthrough
## Introductory notes

This guide explains the decomposition part of the double-sided version of SI2DLA using a toy example. 

The morphemes are: 
```
A → tat 
B → tadt 
C → a 
D → tad
```
The phonological rule is:  **```t → d / a _ a ```**

In words, t becomes d when it occurs between two a's.
Some examples of the rule are: 
```
CA  →  atat   →  adat 
AC  →  tata   →  tada 
CAC →  atata  →  adada
```
The learner only observes the surface mappings, such as:

```
A   → tat 
B   → tadt 
C   → a 
D   → tad 
CA  → adat 
AC  → tada 
CAC → adada 
```
Like the original, the goal of double-sided SI2DLA is to recover two transducers. 

The first, **T_f**, maps morphemes to their underlying forms:
```
A → tat 
B → tadt 
C → a 
D → tad 
```
The second, **T_g**, represents the phonological rule **```t → d / a _ a ```** whose application converts the underlying forms into the observed surface forms. 

Unlike the one-sided version of SI2DLA, the decomposition algorithm constructs a 
three-state phonology transducer. The additional state allows the machine to delay the output of a target symbol until the following symbol has been read.



## OSTIA
The algorithm begins by learning a composed transducer using OSTIA. 
```
T_f = ostia(D,Rho,Sigma) 
```
OSTIA produces a single transducer which simultaneously represents themorphology and the phonology. 

For this example, assume OSTIA returns the following three-state machine:


    State q1: 
        A : ta   → q2 
        B : tadt → q1 
        C : a    → q3 
        D : tad  → q1 
    
    State q2: 
        A : tta   → q2 
        B : ttadt → q1 
        C : da    → q3 
        D : ttad  → q1 
 
    State q3: 
        A : da   → q2 
        B : dadt → q1 
        C : a    → q3 
        D : dad  → q1 
 
    The state outputs are: 
        q1 : λ 
        q2 : t 
        q3 : λ 
 
Notice that the outputs written on the transitions are not always the complete outputs of the machine. 
 
For example, the transition ```q1 → A : ta → q2``` outputs only ```ta```. However, the input ends in q2, whose state output is ```stout(q2) = t```. The complete output is therefore **```ta + t = tat```**.
 
Similarly, ```q2 → A : tta → q2``` produces ```tta + t = ttat```. 
 
The state outputs will become important later, when the algorithm identifies the target state.



## Output Suffixes 

```
OS = { 
    q1 : get_OS(T_f,q1) | {""}, 
    q2 : get_OS(T_f,q2), 
    q3 : get_OS(T_f,q3) 
} 
```
The algorithm now computes the output suffixes, or the set of final output symbols on transitions entering each state, 
 
*Note: the helper function ```suff_1(w)``` returns the last symbol of ```w```.*
 
**State q1:**
 
The incoming transitions are 
```
q1 → B : tadt → q1 
q1 → D : tad → q1 
q2 → B : ttadt → q1 
q2 → D : ttad → q1 
q3 → B : dadt → q1 
q3 → D : dad → q1 
 ```
The corresponding outputs are 
```
tadt 
tad 
ttadt 
ttad 
dadt 
dad 
 ```
Taking the final symbol of each output gives 
 ```
t 
d 
t 
d 
t 
d 
 ```
Therefore, ```OS(q1) = {t,d}```.
 
Since q1 is the initial state, the algorithm also adds the empty string, so
**```OS(q1) = {"",t,d}```**
 
**State q2:**
 
The incoming transitions are 
```
q1 → A : ta → q2 
q2 → A : tta → q2 
q3 → A : da → q2 
 ```
The outputs are 
```
ta 
tta 
da 
```
Their final symbols are 
```
a 
a 
a 
```
Therefore, **```OS(q2) = {a}```**.
 
**State q3:**
 
The incoming transitions are 
```
q1 → C : a → q3 
q2 → C : da → q3 
q3 → C : a → q3 
 ```
The outputs are 
 ```
a 
da 
a 
 ```
Again, every output ends in a. Therefore, **```OS(q3) = {a}```**.
 
**All together,**
```
OS = { 
    q1 : {"",t,d}, 
    q2 : {a}, 
    q3 : {a} 
} 
```
This is the first major difference from the one-sided SI2DLA algorithm. In the 
one-sided algorithm, the output suffixes uniquely identify the role of every state. Here, ```OS(q2) = OS(q3)```.
 
The output suffixes alone are no longer enough to identify the state roles.  

The algorithm must use one additional piece of information. 

## Identifying the Target State

The code first determines which OSTIA state corresponds to the target state. 

*From this point onward, we refer to these states by their roles:
```qd: default state```, ```qe: environment state``` and ```qt: target state```.*

```python
remaining_states = [q1,q2,q3]

if len(T_f.stout[q1]) > 0: 
    corr["qt"] = q1 
elif len(T_f.stout[q2]) > 0: 
    corr["qt"] = q2 
elif len(T_f.stout[q3]) > 0: 
    corr["qt"] = q3 
```
Recall the state outputs. 
```
stout(q1) = λ 
stout(q2) = t 
stout(q3) = λ 
```
Only q2 has a nonempty state output. Therefore, ```corr["qt"] = q2```and ```rroc[q2] = "qt"```. 

The remaining states are now q1 and q3. 

Unlike the one-sided algorithm, the target state is identified using the state outputs rather than the output suffixes. 
The code then replaces the output suffix set of the target state with its delayed output. 
```
OS[corr["qt"]] = {T_f.stout[corr["qt"]][0]} 
```
Since ```corr["qt"] = q2``` and ```stout(q2) = t```, the modified output suffix sets become 
```
OS = { 
    q1 : {"",t,d}, 
    q2 : {t}, 
    q3 : {a} 
} 
```
Notice that the entry for q2 is no longer the set of suffixes on transitions entering q2. 
Instead, it records the delayed symbol stored by the target state. This is what allows the remaining two states to be distinguished like in the original SI2DLA algorithm.



## Choosing the Default and Environment States 

The target state has now been identified. 
The algorithm next classifies the two remaining OSTIA states. 
 
The relevant code is: 
``` python
if len(OS[remaining_states[0]]) > len(OS[remaining_states[1]]): 
    corr["qd"] = remaining_states[0] 
    corr["qe"] = remaining_states[1] 
 
else: 
    corr["qd"] = remaining_states[1] 
    corr["qe"] = remaining_states[0] 
```
The remaining states are **q1** and **q3**. 
 
Their modified output suffix sets are 
```
OS(q1) = {"", t, d} 
OS(q3) = {a} 
```
The sizes of these sets are **```|OS(q1)| = 3 and |OS(q3)| = 1```**
 
As in the original SI2DLA algorithm, the state with the smaller output suffix set becomes the environment state. Therefore, 
```
q3 → qe 
q1 → qd 
```
The correspondence map is 
```
corr = { 
    "qt" : q2, 
    "qd" : q1, 
    "qe" : q3 
} 
``` 
and the reverse correspondence map is 
```
rroc = { 
    q2 : "qt", 
    q1 : "qd", 
    q3 : "qe" 
} 
```
The algorithm has now identified all three states. 



## Computing IS 
 
The code now constructs the input suffix sets. 
```
IS = { 
    "qt" : OS[corr["qt"]], 
    "qe" : OS[corr["qe"]], 
    "qd" : OS[corr["qd"]] 
} 
```
Substituting the values, 
 ```
corr["qt"] = q2 
corr["qe"] = q3 
corr["qd"] = q1 
 ```
gives 
 ```
IS("qt") = {t} 
IS("qe") = {a} 
IS("qd") = {"", t, d} 
 ```
Therefore, 
 ```
IS = { 
    "qt" : {t}, 
    "qe" : {a}, 
    "qd" : {"", t, d} 
} 
 ```
Just as in the original SI2DLA algorithm, these sets determine which state the phonology transducer should enter after reading each symbol. 



## Building d_g 
 
The code now constructs the transition function of T_g. 
```python
d_g = {} 
for q in Q_g: 
    for s in Sigma: 
        ... 
```
The algorithm considers every 
pair consisting of 
* a current state q, and 
* an input symbol s. 
 
For each pair ```(q,s)```, it determines the next state of T_g. 
 
Recall that 
```
Q_g = {qd, qe, qt} 
Sigma = {a, d, t} 
```
and 
 ```
IS(qt) = {t} 
IS(qe) = {a} 
IS(qd) = {"", t, d} 
 ```
Unlike the one-sided SI2DLA algorithm, the next state depends on both the current state and the current input symbol. 
 
The code determines the next state using three tests. 
 
**Step 1:**

The code first checks 
```python
if s in IS["qe"]: 
    d_g[(q,s)] = "qe" 
```
Recall that ```IS(qe) = {a}.```
Therefore, this condition is true only when ```s = a```. 
 
Whenever the current input symbol is a, the next state is initially assigned to qe. So the following transitions are created:
```
(qd,a) → qe 
(qe,a) → qe 
(qt,a) → qe 
 ```

**Step 2:**
 
The code next checks 
```python
if s in IS["qd"]: 
    d_g[(q,s)] = "qd" 
```
Recall that ```IS(qd) = {"", t, d}```. 
 
The empty string is never read as an input symbol, so the only relevant symbols are t and d. 
 
Therefore, whenever ```s = t``` or ```s = d```, the next state is assigned to qd. 
This gives:
```
(qd,t) → qd 
(qe,t) → qd 
(qt,t) → qd 
(qd,d) → qd 
(qe,d) → qd 
(qt,d) → qd 
```
At this point, every transition has been assigned a destination state. However, one of these transitions still needs to be modified.

**Step 3:**

The code now checks 
```python
if s in IS["qt"] and q != "qd" and q != "qt": 
    d_g[(q,s)] = "qt" 
else: 
    d_g[(q,s)] = "qd" 
```
Recall that ```IS(qt) = {t}```, so the first condition requires ```s = t```. 

The remaining conditions require 
```q ≠ qd``` and ```q ≠ qt```. 
Since the only remaining state 
is qe, this condition is true 
only for (qe,t). 

The assignment from Step 2 is therefore overwritten. 
Instead of ```(qe,t) → qd```, we obtain ```(qe,t) → qt```. 

This is the only transition entering the target state. The else branch applies to every other case and assigns the transition to qd. Since these transitions were already assigned to qd in Step 2, the else branch does not change any of the remaining transitions. 

The completed transition function is therefore:
<dl>
<dt><b>From qd: </b></dt>
    <dd>a → qe</dd>
    <dd>d → qd </dd>
    <dd>t → qd </dd>

<dt><b>From qe: </b></dt>
    <dd>a → qe </dd>
    <dd>d → qd </dd>
    <dd>t → qt </dd>

<dt><b>From qt: </b></dt>
    <dd>a → qe </dd>
    <dd>d → qd </dd>
    <dd>t → qd</dd>
</dl>
Notice that the only transition entering qt is ```qe --t--> qt```. This is exactly the situation in which the machine has already seen the left context a and has just read the target t.  

The machine therefore enters the target state and waits to determine whether the following symbol completes the environment. 



## Building o_g 

The code now constructs the 
output function of T_g. 
```python
o_g = {} 
for s in Sigma: 
```
The algorithm computes the outputs one input symbol at a time. 
For each symbol, it first determines the output leaving the default state. It then compares corresponding transitions in the OSTIA transducer to determine the outputs leaving the environment and target states. 

### Initializing the Default State
The first statement inside the loop is ```o_g[("qd",s)] = s```.

Every transition leaving qd initially outputs its input symbol unchanged. 
Therefore, 
```
o_g((qd,a)) = a 
o_g((qd,d)) = d 
o_g((qd,t)) = t 
```
The outputs leaving qe and qt are computed next. 

### Finding the Default Transitions

The code first collects every 
transition leaving the default 
state whose output begins with 
the current input symbol. 
``` python
d_trs = [ 
    tr for tr in T_f.E 
    if tr[0] == corr["qd"] 
    and tr[2][0] == s 
] 
```
Recall that ```corr["qd"] = q1```. 
Thus, d_trs contains transitions 
leaving q1 whose output begins 
with the current symbol.

The algorithm now considers each 
input symbol separately. 

### Symbol t

For ```s = t```
the transitions leaving q1 whose 
outputs begin with t are 
```
q1 → A : ta   → q2 
q1 → B : tadt → q1 
q1 → D : tad  → q1 
```
Each transition produces the 
same computation, so we consider 
only morpheme A. 

The corresponding default 
transition is ```d = q1 → A : ta → q2```.

The code now finds the 
corresponding environment 
transition. 
 ```python
env_tr = [ 
    tr for tr in T_f.E 
    if tr[0] == corr["qe"] 
    and tr[1] == d[1] 
] 
 
env_tr = env_tr[0] 
 ```
Recall that ```corr["qe"] = q3```. The algorithm therefore looks for the transition leaving q3, and reading morpheme A. 
 
This gives ```env_tr = q3 → A : da → q2```.
 
Next, the code finds the corresponding target transition. 
```python
trg_tr = [ 
    tr for tr in T_f.E 
    if tr[0] == corr["qt"] 
    and tr[1] == d[1] 
    and tr[3] == env_tr[3] 
] 
 
trg_tr = trg_tr[0] 
```
Since ```corr["qt"] = q2```, the 
algorithm looks for the 
transition leaving q2, 
reading morpheme A, and ending 
in  the same state as ```env_tr```. 
 This gives ```trg_tr = q2 → A : tta → q2```.

The three corresponding transitions are therefore:
<dl>
<dt><u>Default transition</u></dt>
    <dd>q1 → A : ta → q2</dd>
<dt><u>Environment transition </u></dt>
    <dd>q3 → A : da → q2 </dd>
<dt><u>Target transition</u> </dt>
    <dd>q2 → A : tta → q2 </dd>
</dl>

### Computing the Output for qe
 
The code first computes the output leaving the environment state. 
```python
w_d = d[2] 
w_e = env_tr[2] 
w_s = lncat_format(w_e,w_d[1:]) 
```
For this example, 
```w_d = ta``` and ```w_e = da```.

Since ```w_d[1:] = a```, we obtain ```lncat_format(da,a) = d```. 
 
The code now checks 
```python
if w_s != tuple(s) and w_s != (): 
    o_g[("qe",s)] = "lambda" 
else: 
    o_g[("qe",s)] = w_s 
```
Here, 
```w_s = d``` and ```s = t```. 
Since ```d ≠ t```, the output becomes 
```o_g((qe,t)) = lambda```. 

No output is produced. 

The machine instead waits until 
the following symbol is read. 

### Computing the Output for qt

The code now computes the output 
leaving the target state. 

First, ```w_e = trg_tr[2]```, so ```w_e = tta```. 

The code then reverses the 
target and default outputs. 
```python
w_e_reversed = w_e[::-1] 
w_d_reversed = w_d[::-1] 
```
giving 
```
reverse(tta) = att 
reverse(ta) = at 
```
The longest common prefix of 
these reversed strings is 
```at```. 
Reversing this again gives the longest common suffix of the original strings. So, ```lcs = ta```. 

The code now removes this suffix from the target output:
```w_s = lncat_format(w_e,lcs) + tuple(s)```

Removing ta from tta leaves t. 

The current input symbol is then 
appended, so ```t + t = tt```. 
Therefore, 
```o_g((qt,t)) = tt```. 

The outputs for t are therefore:
<dl>
<dt><b>From qe </b></dt>
    <dd>t : λ </dd>
<dt><b>From qt </b></dt>
    <dd>t : tt</dd>
</dl>

### Symbol a

The algorithm now repeats the same computation for ```s = a```.

The only transition leaving q1 
whose output begins with a is 
```q1 → C : a → q3```. 

The corresponding environment 
and target transitions are 
```q3 → C : a → q3 ``` and ```q2 → C : da → q3```. 
Thus, 
```
w_d = a 
w_e = a 
w_t = da
```
Computing the environment output gives ```lncat_format(a,"") = a```, so ```o_g((qe,a)) = a```. 
 
For the target state, the longest common suffix of ```da``` and ```a``` is ```a```. Removing this suffix leaves ```d```. Appending the current input symbol gives ```da```. Therefore, 
```o_g((qt,a)) = da```. 
 
### Symbol d
 
Finally, consider ```s = d```. 
 
There are no transitions leaving 
q1 whose outputs begin with ```d```. 
 
Thus, ```d_trs = {}```. 
 
The code therefore executes 
```python
if not d_trs: 
    o_g[("qt",s)] = T_f.stout[corr["qt"]] + tuple(s) 
    o_g[("qe",s)] = s 
```
Since ```stout(qt) = t```, we obtain 
``` 
o_g((qe,d)) = d 
o_g((qt,d)) = td
```
 
### The Completed Output Function
 
We have now computed the outputs for every input symbol. 
<dl>
<dt><b>From qd </b></dt>
    <dd>a : a </dd>
    <dd>d : d </dd>
    <dd>t : t </dd>
<dt><b>From qe </b></dt>
    <dd>a : a </dd>
    <dd>d : d </dd>
    <dd>t : λ </dd>
<dt><b>From qt </b></dt>
    <dd>a : da </dd>
    <dd>d : td </dd>
    <dd>t : tt </dd>
</dl>
This completes the construction of o_g. 

## Constructing T_g
 
The code now combines d_g and o_g. 
```python
E_g = [] 
for (q,s) in d_g.keys(): 
    E_g.append((q,s,o_g[(q,s)], d_g[(q,s)])) 
```
Each transition consists of:
* a starting state, 
* an input symbol, 
* an output string, 
* and a destination state. 
 
Putting the transition and 
output functions together gives 
the following transducer:
``` 
From qd 
a : a  → qe 
d : d  → qd 
t : t  → qd 

From qe 
a : a  → qe 
d : d  → qd 
t : λ  → qt 

From qt 
a : da  → qe 
d : td  → qd 
t : tt  → qd 
```
The target state has the state output ```stout(qt) = t```. This output is produced only if the input ends while the machine is still in qt. 




## Testing T_g 
 
We now test T_g on several underlying strings. These examples illustrate the behavior of the completed phonology transducer. 
 
### Example 1 
 
Consider the underlying string ```ata```. 
 
The machine begins in qd. 
 
Reading the first ```a``` gives ```a : a → qe```. The machine outputs ```a``` and enters qe. 
 
Reading t gives ```t : lambda → qt```. No output is produced, and the machine enters qt. 
 
Reading the final a gives ```a : da → qe```.
 
The outputs are therefore ```a + lambda + da = ada```.
 
So, **```ata → ada```**.
 
### Example 2 
 
Now consider ```att```.
 
The machine reads ```a : a → qe``` followed by ```t : lambda → qt```.
Finally, it reads ```t : tt → qd```
 
The outputs are 
```a + lambda + tt = att ```.
 
Therefore, **```att → att```**.
 
The rule does not apply because the delayed ```t``` is not followed by ```a```. 
 
### Example 3 
 
Finally, consider an input ending in ```at```.
 
The machine reads ```a : a → qe``` followed by ```t : lambda → qt```. 
The input now ends while the 
machine is still in qt. 
 
The machine therefore produces the state output ```stout(qt) = t```.
 
The complete output is ```a + lambda + t = at```.
 
Therefore, **```at → at```**.
 
The delayed t is preserved because the required right context never appeared. 
 


## Recovering T_f 
 
The algorithm now modifies the 
original OSTIA transducer to 
recover T_f. 
 
The relevant code is 
```python
mod_e = [] 
 
for tr in T_f.E: 
    if tr[0] == corr["qd"]: 
        if tr[3] == corr["qt"]: 
 
            upd_tr = ( 
                tr[0], 
                tr[1], 
                tr[2] + T_f.stout[corr["qt"]], 
                tr[3] 
            ) 
 
            mod_e.append(upd_tr) 
 
        else: 
 
            mod_e.append(tr) 
```
Recall that 
```corr["qd"] = q1``` and ```corr["qt"] = q2```.
 
The algorithm keeps only the transitions leaving q1. These are:
```
q1 → A : ta   → q2 
q1 → B : tadt → q1 
q1 → C : a    → q3 
q1 → D : tad  → q1 
```
The remaining transitions are 
discarded. 



## Recovering the Underlying Forms 
 
One transition still has an 
incomplete output. 

Consider ```q1 → A : ta → q2```.
 
The transition output is ```ta```. However, the transition ends in q2, whose state output is ```t```. The code therefore appends the delayed output: ```ta + t = tat```. 

The updated transition becomes ```q1 → A : tat → q2```. The remaining transitions do not end in q2, so they are unchanged. Thus, 
```
q1 → B : tadt → q1 
q1 → C : a    → q3 
q1 → D : tad  → q1 
```
The recovered outputs are therefore 
```
A → tat 
B → tadt 
C → a 
D → tad 
```
These are exactly the underlying forms. 



## Simplifying T_f 
 
At this point, the additional states are no longer needed. The states q2 and q3 were introduced only to encode phonological information. 
Once the underlying forms have been recovered, that information is represented entirely by T_g. The remaining transitions can therefore be redirected to a single state. 
 
The transition ```q1 → A : tat → q2```becomes ```q1 → A : tat → q1```
 
Similarly, ```q1 → C : a → q3``` becomes ```q1 → C : a → q1```
 
The transitions 
```q1 → B : tadt → q1``` and ```q1 → D : tad → q1``` already loop to q1 and remain unchanged. 
 
The final morphology transducer 
is therefore:
``` 
State q1: 
A : tat  → q1 
B : tadt → q1 
C : a    → q1 
D : tad  → q1 
```
This transducer maps each morpheme directly to its underlying form. 



## The Final Decomposition 

We have now constructed both transducers. 

The morphology transducer is T_f: 
```
State q1: 
A : tat  → q1 
B : tadt → q1 
C : a    → q1 
D : tad  → q1 
```
The phonology transducer is T_g: 
```
State qd: 
a : a  → qe 
d : d  → qd 
t : t  → qd 

State qe: 
a : a  → qe    
d : d  → qd
t : λ  → qt 

State qt: 
a : da  → qe 
d : td  → qd 
t : tt  → qd 

stout(qt) = t 
```
The composition ```T_f ○ T_g``` is equivalent to the original OSTIA transducer.
