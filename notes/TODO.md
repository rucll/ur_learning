# To-do list

## Features to add


### Dataset generator
- Adding morphotactic restrictions 
- natural classes (might or might not be important)
- test more edge cases (all empty, only filled contexts, blank contexts with filled target and output) 
- The program should provide feedback to the user about a bad input (e.g. Left context "a #" is a bad input)
- potentially offer 2 output methods, one brings up a textbox that you can see immediately and one produces a download like we currently have (Ezra disagrees with this, but it was requested)

### si2dla_gui
- This should be moved into the top folder
- Initial state, state outputs, (final states?,) needs to be marked
- Should be able to save results


## Bugs

### Dataset generator

- si2dla_gui crashes (or has crashed at least once) when run on data output by dataset generator

### si2dla_gui
- Doesn't clear old machines when loading new dataset
- Breaks on `Yagba_Nasalharmony.csv` -- throws error. This is probably because the data is formatted incorrectly. This should be replaced with a dialog box that says "Data could not be parsed, check data format."



