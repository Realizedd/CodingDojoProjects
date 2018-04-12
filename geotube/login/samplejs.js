$(document).ready(function() {
	var formLogin= $('#login'),
		formSignup=$('#signup'),
		formSwitch=$('.switcher'),
		tabLogin=formSwitch.children('li').eq(0).children('a'),
		tabSignup=formSwitch.children('li').eq(1).children('a');
	
	formSwitch.on('click', function(event){
		event.preventDefault();
		( $(event.target).is(tabLogin) ) ? login_selected() : signup_selected();
	});

	function login_selected(){
		formLogin.addClass('is-visible');
		formLogin.addClass('is-selected');
		formSignup.removeClass('is-selected')
		tabSignup.removeClass('is-selected');
		tabLogin.addClass('selected');
		tabSignup.removeClass('selected');
	}
	function signup_selected(){
		formSignup.addClass('is-visible');
		formLogin.removeClass('is-selected');
		formSignup.addClass('is-selected');
		tabLogin.removeClass('selected');
		tabSignup.addClass('selected');
	}
});

