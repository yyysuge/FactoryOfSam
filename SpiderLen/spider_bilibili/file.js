var fs = require('fs');

var path = 'output.txt';
var content = 'Hello World!';
fs.write(path, content, 'w');

phantom.exit();