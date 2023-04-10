
# Molecule Webserver

This project is a website for uploading and viewing molecules as svg files. After selecting elements that you want to use, you can view all sorts of molecules of varying shapes and sizes, from a simple water molecule to a large saturated fat. The elements that represent the atoms of each molecule can be customized to have different colors and sizes. The molecule can also be rotated for different visual perspectives.

This project was initally made for a school course, but has since then been extended and developed to contain additional features.

*Developed by Elman Islam, 2023*

  

# Files
> Folder structure for the molecule webserver project

#### 'molecule-webserver' Directory
```
.
├── bin                 	# Compiled files
├── C                   	# Module for .c files 
├── data   					# Contains .sdf and .svg files (but not .db)
├── src                 	# Source files (alternatively `lib` or `app`)
├── templates           	# Web pages, styles sheets and javascript 
└── makefile				# Compile the program, remove executables 
└── molecule.db				# Database structure for containing molecule data
└── server.py				# Contains python handler class to run the server
└── README.md	
└── README.txt				# Alternative notes for readme	
```

#### 'C' Directory
```
.
├── ...
├── C                    	# Module for .c files
│   └── mol.c         		# Functions for making atoms, bonds and molecules
│   └── mol.h         		# Header for mol.c
│   └── molecule_wrap.c     # Generated swig file 
│   └── molecule.i     		# Preprocessor file for mol.c and mol.h

└── ...
```

#### 'src' Directory
```
.
├── ...
├── src                    	# Source files (alternatively `lib` or `app`)
│   ├── lib         		# Library modules
│   └── MolDisplay.py       # Parse .sdf file and convert to inline svg xml code
│   └── molecule.py     	# Generated swig file for converting c to python
│   └── molsql.py     		# Create and edit SQL database (molecule.db)

└── ...
```
 #### 'templates' Directory
```
.
├── ...
├── templates               # Web pages, styles sheets and javascript 
│   └── add-element.html    
│   └── remove-element.html    
│   └── add-molecule.html    
│   └── view-molecule.html    
│   └── display.html    
│   └── index.html    		# Home page
│   └── script.js     		# Contains ajax for sending form data
│   └── styles.css     		# fancy styling for all pages

└── ...
```

## How to Run
**This program assumes that you are running commands on a linux or mac terminal (ubuntu, MacOS, debian, etc).*

<u><b>To compile the program, open your terminal and follow these instructions:</b></u>

1. Find the molecule-webserver directory in your file explorer and copy the filepath
2. `cd [path/to/molecule-webserver]` ; make sure the slash symbols are / , and not \ . If they aren't, you will have to change them manually, which can be a bit tedious. save the filepath with the / for running the program in the futre
3. `export LD_LIBRARY_PATH=:[path/to/webserver]/src/lib` ; Make sure to type `/src/lib` after pasting the file directory in the command, otherwise the program will produce an error when you run it
4. `make clean` and then `make`
5. `python3 server.py [optional port number]` ; you can type a specified port number if you want, but otherwise the default port is `8000`
6. click on the link that was outputted in the terminal and enjoy the website! 

The `server.py` file contains a main method that creates a server using the http.server python framework. This file is where all of the do_GET and do_POST actions occur, which involve loading different pages and uploading svg data or other information. Think of it as your `main` file for this program.

### Why am I getting an error?
Below are some possible errors you might run into due to incorrect commands or missing resources
* <i><b>ImportError: libmol.so: cannot open shared object file: No such file or directory</b></i>
This happens when your LD_LIBRARY_PATH variable does not correctly direct to the `lib` directory in the project. go back to step 3 and make sure you are correctly assigning the variable to the right filepath
- <i><b>no such module: _molecule</b></i>
      make sure molecule.py is in the src directory, and on line 13,
      change the line "`from . import _molecule`" to "`from .lib import _molecule`"
* <i><b>C/molecule_wrap.c:154:11: fatal error: 'Python.h' file not found</b></i>
	Your system may not have python installed, or the incorrect version is being used. run the following command: `python3 --version` And if nothing comes up you will have to install python with `sudo apt install python3`. But if an output <em>does</em> come up, open the makefile and for the variables `PY_HEADER` and `PY_LIB` (lines 5 and 6), change the `3.9` in the file paths to whatever number was printed when you checked your python3 version.

