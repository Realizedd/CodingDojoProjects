app.controller('DropMenuController', function($scope, $location, $window, userFactory) {
	$scope.login = {};

	$scope.attemptLogin = function() {
		userFactory.attemptLogin($scope.login, function() {
			$scope.login = {};
			$window.location.reload();
		});
	}

	$scope.attemptRegister = function() {
		userFactory.attemptRegister($scope.registration, function() {
			$scope.registration = {};
			$window.location.reload();
		});
	}

	// userFactory.isLoggedIn(function(data) {
	// 	if (data.logged_in) {
	// 		// UNUSED: $('.user-info').html('<a href="#/" id="menu"><i class="fa fa-bars fa-lg" aria-hidden="true"></i></a>');
	// 		$('.user-info').html('<a href="#/" id="menu">SIGN OUT <i class="fa fa-sign-out fa-lg" aria-hidden="true"></i></a>');
	// 	} else {
	// 		$('.user-info').html('<a href="#/" id="menu">SIGN IN <i class="fa fa-arrow-circle-right fa-lg" aria-hidden="true"></i></a>');
	// 	}
	// });
});

app.controller('HomeController', function($scope, $location, userFactory) {
	$scope.user = {};

	userFactory.isLoggedIn(function(data) {
		if (data.logged_in) {
			// $('.user-info').html('<a href="#/" id="menu"><i class="fa fa-bars fa-lg" aria-hidden="true"></i></a>');
			$('.user-info').html('<a href="#/" id="menu">SIGN OUT <i class="fa fa-sign-out fa-lg" aria-hidden="true"></i></a>');
			$scope.user.username = data.username;
		} else {
			$('#side-content-user-info-wrapper').html('<p class="important top-cover">Welcome, User</p><button>Sign up now!</button>');
			$('.user-info').html('<a href="#/" id="menu">SIGN IN <i class="fa fa-arrow-circle-right fa-lg" aria-hidden="true"></i></a>');
		}
	});
});

app.controller('ProfileController', function($scope, $window, $routeParams, userFactory) {
	$scope.user = {};
	$scope.new_comment = {};

	// userFactory.isLoggedIn(function(data) {
	// 	if (data.logged_in) {
	// 		// UNUSED: $('.user-info').html('<a href="#/" id="menu"><i class="fa fa-bars fa-lg" aria-hidden="true"></i></a>');
	// 		$('.user-info').html('<a href="#/" id="menu">SIGN OUT <i class="fa fa-sign-out fa-lg" aria-hidden="true"></i></a>');
	// 	} else {
	// 		$('.user-info').html('<a href="#/" id="menu">SIGN IN <i class="fa fa-arrow-circle-right fa-lg" aria-hidden="true"></i></a>');
	// 	}
	// });

	userFactory.getUser($routeParams.id, function(user) {
		$scope.user = user;
		var date = new Date($scope.user.created_at);
		$scope.user.created_at = monthNames[date.getMonth()] + " " + date.getDate() + ", " + date.getFullYear();

		for (var i in user.comments) {
			var comment = user.comments[i];
			var cDate = new Date(comment.comment_creation);
			var dateStr = monthNames[cDate.getMonth()] + " " + cDate.getDate() + ", " + cDate.getFullYear();
			$('#profile-wall-content-comments').append('<div class="profile-wall-content-comment"><a href="#/members/' + comment.creator_id + '">' + comment.comment_creator + '</a><p>' + comment.comment + '</p><p>' + dateStr + '</p></div>');
		}

		$scope.addComment = function() {
			userFactory.postComment(user.id, $scope.new_comment.comment, function(res) {
				$scope.new_comment = {};
				$window.location.reload();
			});
		}
	});
});

app.controller('ForumController', function($scope, $window, $routeParams, userFactory) {
	
});