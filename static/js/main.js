(function($) { "use strict";

	// if scroll then nav bar issmaller
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
	
	// Animation and theme
	$(document).ready(function() {
  
	  // Load saved theme
	  var savedTheme = localStorage.getItem('theme');
	  if (savedTheme) {
		$("html").attr("data-theme", savedTheme);
		if (savedTheme === "dark") {
		  $("#switch").addClass("switched");
		}
	  } 
	  	// default - light
	  else {
		$("html").attr("data-theme", "light");
		localStorage.setItem('theme', 'light');
	  }
	});
  
	// Menu on hover
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