import sys
import asttokens, ast
from token import tok_name
import string

ESCAPE_STR="\\"
OPEN_P="(%"
CLOSE_P="%)"
TOKEN_FLAGS=["-t"]
LABEL_FLAGS=["-l"]
WHITESPACE_FLAGS=["-nws"]
TO_ESCAPE=[OPEN_P, CLOSE_P]
FLAGS=TOKEN_FLAGS+ LABEL_FLAGS+ WHITESPACE_FLAGS
INCLUDE_TOKENS=any(e in sys.argv for e in TOKEN_FLAGS)
INCLUDE_LABELS=any(e in sys.argv for e in LABEL_FLAGS)
REMOVE_WHITESPACE=any(e in sys.argv for e in WHITESPACE_FLAGS)

def safe_min(iterable, default=None):
	try:
		return min(iterable)
	except ValueError:
		return default

def find_subsexps(ast_, files):
	height = 0
	for node in ast.walk(ast_.tree):
		b,e =ast_.get_text_range(node)
		if b==0 and e==0:
			continue
		yield b,e,height, type(node).__name__
		if INCLUDE_TOKENS:
			for t in ast_.get_tokens(node, include_extra=True):
				yield t[6], t[7], height, tok_name[t[0]]
		height+=1

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
	except FileNotFoundError:
		print("File not found:", f)
		print("Did you mean one of the flags:", " ".join(FLAGS))

def do_file(fname):
	with open(fname) as f:
		source = f.read()
	ast_ = asttokens.ASTTokens(source, parse=True)

	offsets = list(find_subsexps(ast_, [fname]))

	if INCLUDE_LABELS:
		joined = list( (k, h, OPEN_P+t+': ') for k,v,h,t in offsets) + list( (v, -h, CLOSE_P) for k,v,h,t in offsets)
	else:
		joined = list( (k, h, OPEN_P) for k,v,h, t in offsets) + list( (v, -h, CLOSE_P) for k,v,h,t in offsets)
	joined.sort()

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
