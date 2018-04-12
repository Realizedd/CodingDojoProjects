var tasks = require('../controllers/tasks.js');

module.exports = function(app) {
	app.get('/tasks', function(req, res) {
		tasks.show(req, res);
	});

	app.post('/tasks', function(req, res) {
		tasks.add(req, res);
	});

	app.post('/tasks/update', function(req, res) {
		tasks.update(req, res);
	});

	app.post('/tasks/delete', function(req, res) {
		tasks.delete(req, res);
	});
}