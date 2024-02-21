$(document).ready( function () {
	width = window.screen.width;
	height = window.screen.height;
	if (width > 991) {
		function twoElementsDrop(element, child, secondChild) {
		$(element).hover(function () {
			var child1 = $(element).children(child);
			var secChild = $(element).children(secondChild);
			$(element).toggleClass('show');
			child1.attr('aria-expanded', 'true');
			secChild.toggleClass('show');
		}, function () {
			var child1 = $(element).children(child);
			var secChild = $(element).children(secondChild);
			setTimeout(function () {
				$(element).removeClass('show');
				child1.attr('aria-expanded', 'false');
				secChild.removeClass('show');
			}, 300);
		});
	}

	twoElementsDrop('#drop1', '.dropdown-toggle', '.dropdown-menu');
	
	}

	// if (window.screen.width < 736) {
	// 	$('footer').addClass('fixed-bottom');
	// } else if (window.screen.width >= 736) {
	// 	$('footer').addClass('sticky-bottom');
	// }

	// $(window).on('resize', function() {
	// 	if (window.screen.width < 736) {
	// 		console.log("< 736: " + window.screen.width + ", inner: " + window.innerWidth);
	// 		$('footer').removeClass('sticky-bottom');
	// 		$('footer').addClass('fixed-bottom');
	// 	} else if (window.screen.width >= 736) {
	// 		console.log(">= 736: " + window.screen.width + ", inner: " + window.innerWidth);
	// 		$('footer').removeClass('fixed-bottom');
	// 		$('footer').addClass('sticky-bottom');
	// }
	// });

});
