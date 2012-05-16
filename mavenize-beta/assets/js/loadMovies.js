(function($) {
  // Templates
  var movieTemplate = _.template("\
    <% for (var i = 0; i < movies.length; i++) { %>\
      <% var movie = movies[i]; %>\
      <li class='span3' data-next='<%= movie.next %>'>\
        <a class='thumbnail movie' href='<%= movie.url %>' data-original-title='<%= movie.title %>' data-content='<%= movie.synopsis %>...'>\
        <img src='<%= movie.image_url %>' />\
        </a>\
      </li>\
    <% } %> ");

  // Plugin
  $.fn.loadMovies = function(url) {
    listSelector = $(this);
    $.get(url, function(movies) {
      var thumbnails = movieTemplate({ movies: movies });
      $(listSelector).append(thumbnails);
      $(listSelector).trigger('appended');
    });
    
    $('.thumbnails').bind('appended', function() {
      $('.active').find('.thumbnail').popover({ 'placement': 'bottom' });
    });
  }
}) (jQuery);
