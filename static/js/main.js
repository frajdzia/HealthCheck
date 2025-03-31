(function($) { "use strict";

	$(function() {
	  var header = $(".start-style");
	  $(window).scroll(function() {    
		var scroll = $(window).scrollTop();
		if (scroll >= 10) {
		  header.removeClass('start-style').addClass("scroll-on");
		} else {
		  header.removeClass("scroll-on").addClass('start-style');
		}
	  });
	});		
	
	// Animation and Theme Initialization
	$(document).ready(function() {
  
	  // Load saved theme or default to light
	  var savedTheme = localStorage.getItem('theme');
	  if (savedTheme) {
		$("html").attr("data-theme", savedTheme);
		if (savedTheme === "dark") {
		  $("#switch").addClass("switched");
		}
	  } else {
		$("html").attr("data-theme", "light");
		localStorage.setItem('theme', 'light');
	  }
	});
  
	// Menu On Hover
	$('body').on('mouseenter mouseleave','.nav-item',function(e){
	  if ($(window).width() > 750) {
		var _d=$(e.target).closest('.nav-item');_d.addClass('show');
		setTimeout(function(){
		  _d[_d.is(':hover')?'addClass':'removeClass']('show');
		},1);
	  }
	});	
	
	// Switch light/dark
	$("#switch").on('click', function () {
	  if ($("html").attr("data-theme") === "dark") {
		$("html").attr("data-theme", "light");
		$("#switch").removeClass("switched");
		localStorage.setItem('theme', 'light');
	  } else {
		$("html").attr("data-theme", "dark");
		$("#switch").addClass("switched");
		localStorage.setItem('theme', 'dark');
	  }
	});  
	
  })(jQuery);