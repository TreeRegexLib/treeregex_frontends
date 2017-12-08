# TreeRegex Frontends

This repo contains a set of frontends to turn source code into serialized trees (abbreviated 'sexp').

Each folder contains a frontend to change source code into a serialized tree.  The name of the folder indicates the language of the source code that can be transformed into a serialized tree.  These are listed below.  The implementation of the frontend may not be in the same language as the input to the frontend (e.g. the C++ to serialized tree implementation is in Python).  Each folder describes the installation requirements and supported flags for that frontend in the README.md file.

To run a frontend on a file, specify the filename on the command line, e.g.:

  $ python cpp_to_sexp.py test.cpp
 
 Will run the C++ to serailized tree converter on the `test.cpp` file and create a file named `test.cpp.sexp` with the serailized tree in it.  Flags to the frontend, if they are supported, can be given before or after the input file name.

The following frontends are available:
* C/C++/Objective-C (all co-located in the cpp folder)
* JavaScript
* Python 2&3
