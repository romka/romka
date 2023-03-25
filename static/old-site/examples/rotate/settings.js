$(document).ready(function() {
	$('#image').rotate(-25);
	$('#image2').rotate({angle:15});	
/*
	var rot=$('#image3').rotate({
	bind:
		[
			{"mouseover":function(){rot.rotateAnimation(35);}},
			{"mouseout":function(){rot.rotateAnimation(0);}}
		]
	});

*/
	var rot=$('#image3').rotate({maxAngle:25,minAngle:-55,
		bind:
		[
			{"mouseover":function(){rot[0].rotateAnimation(85);}},
			{"mouseout":function(){rot[0].rotateAnimation(-35);}}
		]
	});

});

