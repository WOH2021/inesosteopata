$('#knowmore').on('click', function(e) {
    e.preventDefault();
    $('html, body').animate({
      scrollTop: $('#about').offset().top
    }, 600); // 600ms scroll duration
  });