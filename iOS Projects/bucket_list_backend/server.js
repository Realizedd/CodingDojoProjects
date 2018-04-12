var express = require('express');
var body_parser	= require('body-parser');

var app	= express();

app.use(body_parser.json());

require('./server/config/mongoose.js');
require('./server/config/routes.js')(app);

app.listen(5000, function() {
	console.log('[bucket_list_backend] Listening on port 5000');
});