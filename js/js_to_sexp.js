

var esprima = require('esprima');
var fs = require('fs');
var file = process.argv[2];

fs.readFile(file, 'utf8', function(err, data){
	if(err) {
		return console.log(err);
	}

	var offsets = [];
	esprima.parseScript(data, { range: true }, function (node, meta) {
		offsets.push(node.range);
	});

	var starts = offsets.map(function(a){ return a[0] });
	var ends = offsets.map(function(a){ return a[1] });

	var joined = starts.map(function(a){ return [a, "(%"]}).concat(ends.map(function (a){ return [a,"%)"]}));
	joined.sort(function (a,b){
		if (a[0] == b[0]){
			if(a[1] < b[1]){
				return -1;
			} else if (a[1] == b[1]){
				return 0;
			} else { return 1; }
		}
		if (a[0] < b[0]){ return -1; }
		return 1;
	});

	console.log(joined);
	var out_test = "";
	var last = 0;
	joined.forEach(function(a){
		out_test += data.substring(last,a[0]) + a[1];
		last = a[0];
	});
	out_test+=data.substring(last);

	fs.writeFile(file+".sexp", out_test, function(err){
		if(err){
			return console.log(err);
		}
	});

	console.log("BEFORE-------\n");
	console.log(data);
	console.log("AFTER--------\n");
	console.log(out_test);
});
