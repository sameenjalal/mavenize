$(document).ready(function () {
  var template = " \
    <% for (var i = 0; i < movies.length; i++) { %> \
      <% var movie = movies[i]; %> \
      <li class='span3'> \
        <a class='thumbnail movie' href='<%= movie.url %>' data-original-title='<%= movie.title %>' data-content='<% movie.synopsis %>...'> \
        <img src='<%= movie.image_url %>' /> \
        </a> \
      </li> \
    <% } %> ";

  $('#filters a[href="#week"]').one("click", function() {
    $.get('/movies/week/1', function(movies) {
      var thumbnails = _.template(template, { movies: movies });
      $('#week .thumbnails').append(thumbnails);
    });
  });

  $('#filters a[href="#month"]').one("click", function() {
    $.get('/movies/month/1', function(movies) {
      var thumbnails = _.template(template, { movies: movies });
      $('#month .thumbnails').append(thumbnails);
    });
  });
  
  $('#filters a[href="#alltime"]').one("click", function() {
    $.get('/movies/alltime/1', function(movies) {
      var thumbnails = _.template(template, { movies: movies });
      $('#alltime .thumbnails').append(thumbnails);
    });
  });
});
