$(document).ready(function () {
	$('.carousel').carousel({interval: 10000});

	var loc = decodeURI(location);
	var value = loc.split("?");
	var kvpair = value[1];
	var res = kvpair.split("=");
	var anime = res[1];

	var c = 0;
	for (var j = 0; j < popular.length; j++) {
		position = popular[j];
		var an = position[0];
		var chapter = position[1];
		var chap_num = position[2];
		var link = position[3];
		var min = position[4];
		var sec = position[5];
		var desc = position[6];
		var vid_link = position[7];
		if (desc == "") {
			desc = "(no description was found).";
		}
		if (anime == an) {
			$('.carousel-inner').append('<div class="carousel-item container"><h1 class="anime-title">' + an + '</h1><h3 class="anime-title">Chapter '+ chap_num +': '  + '</h3><img class="d-block carousel-image" src="'+link +'" alt="Third slide"/>\
			<div class="container description">'+ desc +'<section><a class="watch" href="'+ vid_link +'"> (Watch now !)</a></section></div></div>');
			if ( c < 1 ) {
				$('.nav-title').append(an);
			}	
			if (c < 50) {
			$('.carousel-indicators').append('<li class="select" data-target="#mycarousel" data-slide-to="' + c + '"></li>');
			}
			if (c < 1) {
			$('.carousel-item').toggleClass('active');
			$('.select').toggleClass('active');
			}
			c++;
		}
	}
});