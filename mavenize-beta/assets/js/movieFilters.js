$(document).ready(function () {
  var template = " \
    <% for (var i = 0; i < movies.length; i++) { %> \
      <% var movie = movies[i]; %> \
      <li class='span3' data-next='<%= movie.next %>'> \
        <a class='thumbnail movie' href='<%= movie.url %>' data-original-title='<%= movie.title %>' data-content='<% movie.synopsis %>...'> \
        <img src='<%= movie.image_url %>' /> \
        </a> \
      </li> \
    <% } %> ";
  
  // Helper functions
  var loadMovies = function(timePeriod, page) {
    var url = '/movies/' + timePeriod + '/' + page;
    var listSelector = '#' + timePeriod + ' .thumbnails';
    $.get(url, function(movies) {
      var thumbnails = _.template(template, { movies: movies });
      $(listSelector).append(thumbnails);
    });
  }

  // Initial movies
  loadMovies('today', 1);

  // Initial listeners
  $('#filters a[href="#week"]').one("click", function() {
    loadMovies('week', 1);
  });
  $('#filters a[href="#month"]').one("click", function() {
    loadMovies('month', 1)
  });
  $('#filters a[href="#alltime"]').one("click", function() {
    loadMovies('alltime', 1);
  });

  // Infinite scrolling
  $(window).scroll(function() {
    var break_point = $(document).height() - ($(window).height() * 1.02);
    if ($(window).scrollTop() >= break_point) {
      var timePeriod = $('.tab-content').find('.active').attr('id');
      var nextPage = $('#'+timePeriod+' ul li:last').attr('data-next');
      if (nextPage) {
        loadMovies(timePeriod, nextPage);
      }
    }
  });
});
