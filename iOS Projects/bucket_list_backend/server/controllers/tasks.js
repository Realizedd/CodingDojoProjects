var mongoose = require('mongoose');
var Task 	 = mongoose.model('Task');

module.exports = {

	show: function(req, res) {
		Task.find('{}', function(error, data) {
			res.json(data);
		});
	},

	add: function(req, res) {
		var newTask = new Task({objective: req.body.objective});
		newTask.save(function(error, task) {
			res.json(task);
		});
	},

	update: function(req, res) {
		Task.findOne({_id: req.body.id}, function(error, task) {
			task.objective = req.body.objective;
			task.save(function(error, task) {
				res.json(task);
			});
		});
	},

	delete: function(req, res) {
		Task.remove({_id: req.body.id}, function(error) {
			res.json(req.body);
		});
	}
};