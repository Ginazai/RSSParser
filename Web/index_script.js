$(document).ready(function () {
	$('.carousel').carousel({interval: 10000});

    var x = 0;
	for (var i = 0; i < popular.length; i++) {
		var div = document.getElementById('poorme')
   	 	var place = popular[i];
		var anime = place[0];
		var chapter = place[1];
		var chap_num = place[2];
		var link = place[3];
		var min = place[4];
		var sec = place[5];
		var desc = place[6];
		var vid_link = place[7];
		if (desc == "") {
			desc = "(no description was found).";
		}
		$('.carousel-inner').append('<div class="carousel-item container"><h1 class="anime-title">' + anime + '</h1><h3 class="anime-title">'+ chap_num +': ' + chapter + '</h3><img class="d-block carousel-image" src="'+link +'"/>\
			<div class="container description">'+ desc +'<section><a class="watch" href="'+ vid_link +'"> (Watch now !)</a></section></div></div>');
		if (i < 50) {
			$('.carousel-indicators').append('<li class="select" data-target="#mycarousel" data-slide-to="' + x + '"></li>');
		}
		if (x < 1) {
			$('.carousel-item').toggleClass('active');
			$('.select').toggleClass('active');
		}
		x++;
	}
});