import sys
import clang.cindex
import pprint

CXX_INCLUDES="/usr/include", "/usr/include/c++"

def find_subsexps(node, files):
	#print(node.kind, node.displayname, node.extent)
	if node.extent.start.file is not None and node.extent.start.file.name in files:
		ret = [(node.extent.start.offset, node.extent.end.offset)]
	else:
		ret = []
	children = list(node.get_children())
	for c in children:
		ret.extend(find_subsexps(c, files))
	return ret

def main():

	index = clang.cindex.Index.create()
	args = ['-x','c++']
	for a in CXX_INCLUDES:
		args.extend(['-I', a])
	tu = index.parse(sys.argv[1], args=args)

	diagnostics = list(tu.diagnostics)
	if len(diagnostics) > 0:
		print("There were parse errors")
		pprint.pprint(diagnostics)

	offsets = list(find_subsexps(tu.cursor, [sys.argv[1]]))

	starts = list(k for k,v in offsets)
	ends = list(v for k,v in offsets)

	#starts.sort()
	#ends.sort()
	joined = list( (t, "(%") for t in starts) + list( (t, "%)") for t in ends)
	joined.sort()
	#print(joined)

	with open(sys.argv[1]) as f:
		data = f.read()
	with open(sys.argv[1]+".sexp", "w") as f:
		out_data = ""
		last = 0
		for p, s in joined:
			out_data += data[last:p]+s
			last = p
		out_data += data[last:]
		f.write(out_data)
	print("BEFORE------------\n")
	print(data)
	print("AFTER------------\n")
	print(out_data)

main()

