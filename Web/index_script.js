$(document).ready(function () {
	$('.carousel').carousel({interval: 10000});
    var x = 0;
	for (var i = 0; i < popular.length; i ++) {
		var div = document.getElementById('poorme')
   	 	var place = popular[i];
		var anime = place[0];
		var chapter = place[1];
		var chap_num = place[2];
		var link = place[3];
		var min = place[4];
		var sec = place[5];
		var desc = place[6];
		$('.carousel-inner').append('<div class="carousel-item container"><h1 class="anime-title">' + anime + '</h1><h3 class="anime-title">Chapter '+ chap_num +': ' + chapter + '</h3><img class="d-block carousel-image" src="'+link +'" alt="Third slide"'+'/'+'/>\
			<div class="container description">'+ desc +'</div></div>');
		if (i < 80) {
			$('.carousel-indicators').append('<li data-target="#mycarousel" data-slide-to="' + x + '" class="active"></li>');
		}
		if (x < 1) {
			$('.carousel-item').toggleClass('active');
		}
		x++;
	}
});