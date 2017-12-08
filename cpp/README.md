# C/C++ frontend

This frontend converts C/C++/ObjectiveC to serialized tree form.  To run it, you must have the libclang python bindings installed (see `requirements.txt`).  The script must be run with Python2 for the libclang version specified in the requirements.txt file (later versions work with Python 3).

It supports the following flags:

	`-nws` which removes whitespace
	`-l` which labels each subtree
	`-t` which does token-level subtrees (instead of just grammar level subtrees)
	`--language=*lang*` which treats the source file as *lang* language (supported: c++, c, objective-c).

NOTE: This frontend assumes that all header files necessary for compilation are in standard paths.  These paths are in the `INCLUDES` variable in `cpp_to_sexp.py` for different languages.  If you need a different path, specify it there.  objective-c will probably require a change to the include paths in the source file (it has different install paths on different machines).
