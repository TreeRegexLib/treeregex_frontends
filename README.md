# TreeRegex Frontends

This repo contains a set of frontends to turn source code into serialized trees (abbreviated 'sexp').

Each folder contains a frontend to change source code into a serialized tree.  The name of the folder indicates the language of the source code that can be transformed into a serialized tree.  These are listed below.  The implementation of the frontend may not be in the same language as the input to the frontend (e.g. the C++ to serialized tree implementation is in Python).  Each folder describes the installation requirements for that frontend in the README.md file.

The following frontends are available:
* C/C++/Objective-C (all co-located in the cpp folder)
* JavaScript
* Python 2&3
