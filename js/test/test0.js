

var esprima = require('esprima');
var fs = require('fs');
var file = process.argv[2];

var subsexps = [];
var file_contents = fs.readFile(file);
ast = esprima.parseScript(file_contents, { range: true }, function (node, meta) {
	subsexps.push(node.range);
});

console.log(subsexps);
