const monthNames = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"];

var app = angular.module('forums', ['ngRoute']);

app.config(function($routeProvider) {
	$routeProvider
	.when('/', {
		templateUrl: '/partials/home.html'
	})
	.when('/forum', {
		templateUrl: '/partials/forum.html'
	})
	.when('/chat', {
		templateUrl: '/partials/chat.html'
	})
	.when('/members/:id', {
		templateUrl: '/partials/profile.html'
	})
	.otherwise({
		redirectTo: '/'
	});
});