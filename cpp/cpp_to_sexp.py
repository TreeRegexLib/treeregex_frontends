from __future__ import print_function
import sys
import clang.cindex
import pprint
import string

ESCAPE_STR="\\"
OPEN_P="(%"
CLOSE_P="%)"
TOKEN_FLAGS=["-t"]
LABEL_FLAGS=["-l"]
WHITESPACE_FLAGS=["-nws"]
LANGUAGE_FLAGS=["--lang=c++", "--lang=c", "--lang=objective-c"]
TO_ESCAPE=[OPEN_P, CLOSE_P]
FLAGS=TOKEN_FLAGS+ LABEL_FLAGS+ WHITESPACE_FLAGS
INCLUDE_TOKENS=any(e in sys.argv for e in TOKEN_FLAGS)
INCLUDE_LABELS=any(e in sys.argv for e in LABEL_FLAGS)
REMOVE_WHITESPACE=any(e in sys.argv for e in WHITESPACE_FLAGS)
LANG=next((x for x in sys.argv if x in LANGUAGE_FLAGS), "--lang=c++").split("=")[1]

INCLUDES={'c++':["/usr/include", "/usr/include/c++"], 'c':['/usr/include/'], 'objective-c':['/usr/include/']}

def safe_min(iterable, default=None):
	try:
		return min(iterable)
	except ValueError:
		return default


def find_subsexps(node, files, tu):
	out = _find_subsexps(node, files)
	if INCLUDE_TOKENS:
		inf = float('inf')
		for t in tu.get_tokens(extent = node.extent):
			out.append((t.extent.start.offset, t.extent.end.offset, inf, t.kind.name))
	return out

def _find_subsexps(node, files, height=0):
	if node.extent.start.file is not None and node.extent.start.file.name in files:
		ret = [(node.extent.start.offset, node.extent.end.offset, height, node.kind.name)]
	else:
		ret = []
	children = list(node.get_children())
	for c in children:
		ret.extend(_find_subsexps(c, files, height+1))
	return ret

def escape(s):
	index = safe_min(list(filter(lambda a:a[0]>=0, ((s.find(e),e) for e in TO_ESCAPE))), default=(-1,None))
	out = ""
	while index[0] != -1:
		out+=s[:index[0]]+ESCAPE_STR+index[1]
		s = s[index[0]+len(index[1]):]
		index = safe_min(list(filter(lambda a:a[0]>=0, ((s.find(e),e) for e in TO_ESCAPE))), default=(-1,None))
	out+=s
	if REMOVE_WHITESPACE:
		return "".join(filter(lambda a : a not in string.whitespace, out))
	return out

def main():
	files = list(filter(lambda a: a not in FLAGS, sys.argv[1:]))
	try:
		for f in files:
			do_file(f)
	except clang.cindex.TranslationUnitLoadError:
		print("File not found:", f)
		print("Did you mean one of the flags:", " ".join(FLAGS))

def do_file(fname):
	index = clang.cindex.Index.create()
	args = ['-x','c++']
	for a in INCLUDES[LANG]:
		args.extend(['-I', a])
	tu = index.parse(fname, args=args)

	offsets = list(find_subsexps(tu.cursor, [fname], tu))

	if INCLUDE_LABELS:
		joined = list( (k, h, OPEN_P+t+': ') for k,v,h,t in offsets) + list( (v, -h, CLOSE_P) for k,v,h,t in offsets)
	else:
		joined = list( (k, h, OPEN_P) for k,v,h, t in offsets) + list( (v, -h, CLOSE_P) for k,v,h,t in offsets)
	joined.sort()

	with open(fname) as f:
		source = f.read()
	with open(fname+".sexp", "w") as f:
		out_source = ""
		last = 0
		for p, _, s in joined:
			out_source += escape(source[last:p])+s
			last = p
		out_source += source[last:]
		f.write(out_source)
	#print(out_source, end='')

if __name__ == "__main__":
	main()
