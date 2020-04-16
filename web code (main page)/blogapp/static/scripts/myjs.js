$(document).ready(function(){
	// add all event handlers here
	console.log("Adding event handlers");
	//id=username in signup.html
	$("#username").on("change", check_username);
	$("#email").on("change", check_email);
	$("#submit").mouseover(function(){
		$(this).find("input").css("background-color","yellow");
		$(this).find("input").css("font-size","large");
		$(this).find("input").css("width","1000px");
	});
	$("#submit").mouseout(function(){
		$(this).find("input").css("background-color","white");
	});
	console.log("function registered");
});

function check_username(){
	// get the source element
	console.log("check_username called");
	var chosen_user = $(this).find("input");
	console.log("User chose: " + chosen_user.val());
	
	$("#checkuser").removeClass();
	$("#checkuser").html('<img src="static/style/images/loading.gif")>');
	
	// ajax code 
	$.post('/checkuser', {
		'username': chosen_user.val() //field value being sent to the server
	}).done(function (response){
		var server_response = response['text']
		var server_code = response['returnvalue']
		var u=/^[a-zA-Z0-9_]+$/;
		if (server_code == 0 && u.test(chosen_user.val()) == true){ // success: Username does not exist in the database
			$("#email").focus();
			$("#checkuser").html('<span>' + server_response + '</span>');
			$("#checkuser").addClass("success");
		}else if (server_code == 0 && u.test(chosen_user.val()) == false) {
			chosen_user.val("");
			chosen_user.focus();
			$("#checkuser").html('<span>' + "Username format is not correct" + '</span>');
			$("#checkuser").addClass("failure");
		}else { // failure: Username already exists in the database
			chosen_user.val("");
			chosen_user.focus();
			$("#checkuser").html('<span>' + server_response + '</span>');
			$("#checkuser").addClass("failure");
		}
	}).fail(function() {
		$("#checkuser").html('<span>Error contacting server</span>');
		$("#checkuser").addClass("failure");
	});
	// end of ajax code
	
	console.log("finished check_username");
}

function check_email(){
		// get the source element
	console.log("check_email called");
	var chosen_email = $(this).find("input");
	console.log("Email chosen: " + chosen_email.val());
	
	$("#checkemail").removeClass();
	$("#checkemail").html('<img src="static/style/images/loading.gif")>');
	
	// ajax code 
	$.post('/checkemail', {
		'email': chosen_email.val() //field value being sent to the server
	}).done(function (response){
		var server_response = response['text']
		var server_code = response['returnvalue']
		var email=/^([A-Za-z0-9\!\#\$\%\&\'\*\+\-\/\=\?\^\_\`\{\|\}\~]+)(\.){0,1}([A-Za-z0-9\!\#\$\%\&\'\*\+\-\/\=\?\^\_\`\{\|\}\~]+)(\@){1}([A-Za-z0-9\!\#\$\%\&\'\*\+\-\/\=\?\^\_\`\{\|\}\~]+)(\.){1}([A-Za-z0-9\!\#\$\%\&\'\*\+\-\/\=\?\^\_\`\{\|\}\~]+)$/i;
		if (server_code == 0 && email.test(chosen_email.val()) == true){ 
		// success: Email does not exist in the database
			$("#password").focus();
			$("#checkemail").html('<span>' + server_response + '</span>');
			$("#checkemail").addClass("success");
		}else if (server_code == 0 && email.test(chosen_email.val()) == false) {
			chosen_email.val("");
			chosen_email.focus();
			$("#checkemail").html('<span>' + "Email format is not correct" + '</span>');
			$("#checkemail").addClass("failure");
		}else { 
		// failure: Email already exists in the database
			chosen_email.val("");
			chosen_email.focus();
			$("#checkemail").html('<span>' + server_response + '</span>');
			$("#checkemail").addClass("failure");
		}
	}).fail(function() {
		$("#checkemail").html('<span>Error contacting server</span>');
		$("#checkemail").addClass("failure");
	});
	// end of ajax code
	
	console.log("finished check_email");
}
