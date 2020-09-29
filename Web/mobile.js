$(document).ready(function () {
	var an_link = {}
	for (var i = 0; i < popular.length; i++) {
		pos = popular[i];
		nm = pos[0];
		link = pos[3];
		an_link[nm] = link;
	}
	console.log(an_link);
	for (var j = 0; j < animes.length; j++) {
		var position = animes[j];
		var anime = position[0];
		if (anime in an_link) {
			var to_insert = an_link[anime];
			$('.anime-list').append('<div class="container"><a href="anime.html?anime=' + encodeURI(anime) + '"><img class="mobile-img" src="'+ to_insert +'"/></a><li><a class="anime" href="anime.html?anime=' + encodeURI(anime) + '">' + anime + '</a></li></div>');
		}
	}
});