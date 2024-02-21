$(document).ready(function () {
	var check = [];
	for (var i = 0; i < popular.length; i++) {
		pos = popular[i];
		nm = pos[0];
		check.push(nm);
	}
	c = 0;
	for (var j = 0; j < animes.length; j++) {
		var position = animes[j];
		var anime = position[0];
		if (check.includes(anime)) {
			if (c == animes.length - 1) {
				$('.dropdown-menu').append('<div class="dropdown-item"><a href="anime.html?anime=' + encodeURI(anime) + '" class="anime">' + anime + '</a></div>');
			} else {
				$('.dropdown-menu').append('<div class="dropdown-item"><a href="anime.html?anime=' + encodeURI(anime) + '" class="anime">' + anime + '</a></div><div class="dropdown-divider"></div>');
			}
		}
		c++;
	}
});