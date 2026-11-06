# ur_learning

This is a repository of implementations of algorithms for the induction of phonological grammars and underlying forms from morphophonological paradigms. 
These learners are based on the _subregular hypothesis_ that there are strong computational restrictions on phonological cognition (see [Heinz 2018](http://jeffreyheinz.net/papers/Heinz-CNPG-2016.pdf)).
This work is part of the research supported by [NSF Grant #2416184](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2416184) (PIs: [Jane Chandlee](https://www.haverford.edu/users/jchandlee), [Jeffrey Heinz](https://www.jeffreyheinz.net/), and [Adam Jardine](https://adamjardine.net/))

The Simplex Input Strictly 2-Local Decomposition Learning Algorithm of [Hua & Jardine 2021](https://github.com/rucll/ur_learning/blob/main/papers/huajardine2021si2dla.pdf) is implemented in [si2dla.py](si2dla.py).

For a user-friendly version with a graphical interface, run `si2dla_gui.py` in the [/dom_inf_si2dla_gui/](`https://github.com/rucll/ur_learning/tree/main/dom_inf_si2dla_gui`) folder.

Guides for can be found in the [/documentation/] folder.

Example datasets can be found in the [/data/](https://github.com/rucll/ur_learning/tree/main/data) folder.

This code was developed at the Rutgers University [Computational Linguistics Lab](https://rucll.github.io/). Contributors:

- [Adam Jardine](https://adamjardine.net/)
- Neha Jeyaram
- Manish Kandepalli
- Ezra Anthony
- Eli Franz
- Ben Evans

`ostia.py`, `fst_object.py`, and `helper.py` courtesy of [@alenaks](https://github.com/alenaks)'s SigmaPie package.
