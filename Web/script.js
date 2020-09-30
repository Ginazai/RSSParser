$(document).ready( function () {
	var width = window.innerWidth;
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
});
