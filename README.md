# ur_learning
Algorithms based on subregular hypothesis for induction of phonological grammars and sets of underlying forms from morphophonological paradigms. (In progress.)

`ostia.py`, `fst_object.py`, and `helper.py` courtesy of [@alenaks](https://github.com/alenaks)'s SigmaPie package. 

The Simplex Input Strictly 2-Local Decomposition Learning Algorithm of [Hua & Jardine 2021](https://github.com/rucll/ur_learning/blob/main/papers/huajardine2021si2dla.pdf) is implemented in `si2dla.py`.

Other files are experimental variations on this algorithm:

File  | Description 
-- | --
`so2dla.py` | An [Output Strictly 2-Local](https://aclanthology.org/W15-2310/) version of the SI2DLA
`fsi2dla.py` | A featural version of the SI2DLA 
`features.py` | Some code to work with features

The file `testing.py` contains some test data sets; this can be run from the command line to see how the algorithms perform.
