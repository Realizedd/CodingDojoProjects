var mongoose = require('mongoose');

var TaskSchema = new mongoose.Schema( {
	objective: {type: String, required: true},
}, {timestamps: true} );

mongoose.model('Task', TaskSchema);