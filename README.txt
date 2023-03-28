CIS 2750 
Assignment 3
Elman Islam
Student ID : 1126272

To compile: make
If a compile error states "the library path cannot be found", enter the following:
  export LD_LIBRARY_PATH=:/mnt/c/Users/Elman/Downloads/UofG/2750w23/A2

To run MolDisplay: python3 MolDisplay
  Then enter 'localhost:56272' in the web browser
  Upload an sdf file of your choice
  An svg will be created on the page

To run molsql: python3 molsql



Note: On my desktop, I could not download python3.7 as I kept getting
an error stating that "Package python3.7 is not available, but is referred to by another package."
To workaround this, I made the paths for my variables go to python3.9 instead of python3.7
(see makefile).

TESTS AND COMMENTS 
  - test the comp_bonds and qsort functions
  - Add comments
  - Don't forget to change file paths from 'python3.9'
    to 'python3.7m' when testing on school server and before submitting
  


QUESTIONS
When I compile make, I get a warning message indicating that the 
'-dynamiclib' library tag is unused. Is this ok?

Should I make a command in my makefile that creates the molecule_wrap.c and molecule.py
files with swig, or will you already have the files ready when you test my program?


sources for html and css: https://getcssscan.com/css-box-shadow-examples



