import sys
import asttokens, ast

def find_subsexps(ast_, files):
	for node in ast.walk(ast_.tree):
		b,e =ast_.get_text_range(node)
		if b != e:
			yield b,e

def main():
	with open(sys.argv[1]) as f:
		source = f.read()
	ast_ = asttokens.ASTTokens(source, parse=True)

	offsets = list(find_subsexps(ast_, [sys.argv[1]]))
	starts = list(k for k,v in offsets)
	ends = list(v for k,v in offsets)

	joined = list( (t, "(%") for t in starts) + list( (t, "%)") for t in ends)
	joined.sort()
	print(joined)

	with open(sys.argv[1]+".sexp", "w") as f:
		out_source = ""
		last = 0
		for p, s in joined:
			out_source += source[last:p]+s
			last = p
		f.write(out_source)
	print("BEFORE------------\n")
	print(source)
	print("AFTER------------\n")
	print(out_source)

main()

