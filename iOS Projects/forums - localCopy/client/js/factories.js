app.factory('userFactory', function($http) {
	var factory = {};

	factory.isLoggedIn = function(callback) {
		$http.get('/self').then(function(res) {
			callback(res.data);
		});
	}

	factory.attemptLogin = function(info, callback) {
		$http.post('/login', info).then(function(res) {
			callback();
		});
	}

	factory.attemptRegister = function(info, callback) {
		$http.post('/register', info).then(function(res) {
			callback();
		});
	}

	factory.logout = function(callback) {
		$http.post('/logout').then(function(res) {
			callback();
		});
	}

	factory.getUser = function(id, callback) {
		$http.get('/users/' + id).then(function(res) {
			callback(res.data);
		});
	}

	factory.postComment = function(id, comment, callback) {
		$http.post('/users/' + id, {comment: comment}).then(function(res) {
			callback(res.data);
		});
	}

	return factory;
});