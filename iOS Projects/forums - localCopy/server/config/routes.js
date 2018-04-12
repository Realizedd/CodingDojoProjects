// Declare controllers here
var users = require('./../controllers/users.js');
var comments = require('./../controllers/comments.js');

module.exports = function(app, pool) {

	app.get('/users/:id', function(req, res) {
		users.getOne(req, res, pool);
	});

	app.post('/users/:id', function(req, res) {
		comments.create(req, res, pool);
	});

	app.get('/self', function(req, res) {
		users.self(req, res, pool);
	});

	app.post('/register', function(req, res) {
		users.register(req, res, pool);
	});

	app.post('/login', function(req, res) {
		console.log(req.session);
		users.login(req, res, pool);
	});

	app.post('/logout', function(req, res) {
		console.log(req.session);
		users.logout(req, res);
	});
}