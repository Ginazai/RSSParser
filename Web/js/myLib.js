$(document).ready( 

	function () {

		function toggleDropdown(item){
			$(item).hover(function() {
				var menu = $(item).children('.dropdown-menu');
				var aria = $(item).children('#navbarDropdown');
				$(item).toggleClass('show');
				menu.toggleClass('show');
				aria.attr('aria-expanded', 'true');
			}, function() {
				var menu = $(item).children('.dropdown-menu');
				var aria = $(item).children('#navbarDropdown');
				setTimeout(function() {
					$(item).removeClass('show');
					menu.removeClass('show');
					aria.attr('aria-expanded', 'false');
				}, 90);
			});
		} 

		toggleDropdown('#drop1');
		toggleDropdown('#drop2');
		toggleDropdown('#drop3');

		function toggleDropright(param) {
			$(param).hover(function () {
				var button = $(param).children('.dropright-button');
				var menu = $(param).children('#secondary-menu');
				var item = $(menu).children('#secondary-item');
				button.attr('aria-expanded', 'true');
				menu.toggleClass('show');
			}, function () {
				button = $(param).children('.dropright-button');
				var menu = $(param).children('#secondary-menu');
				setTimeout(function () {
					$(button).attr('aria-expanded', 'false')
					menu.removeClass('show');
				}, 90);
			});
		}

		toggleDropright('.dropright');

});