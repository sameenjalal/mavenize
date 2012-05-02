$(document).ready(function () {
  // Global Variables
  var currentParameters = '';

  // Templates
  var movieTemplate = _.template(" \
    <% for (var i = 0; i < movies.length; i++) { %> \
      <% var movie = movies[i]; %> \
      <li class='span3' data-next='<%= movie.next %>'> \
        <a class='thumbnail movie' href='<%= movie.url %>' data-original-title='<%= movie.title %>' data-content='<%= movie.synopsis %>...'> \
        <img src='<%= movie.image_url %>' /> \
        </a> \
      </li> \
    <% } %> ");

  var filtersTemplate = _.template(" \
    <div class='modal-header'> \
      <a class='close' data-dismiss='modal'>×</a> \
      <h3>Filter Your Results</h3> \
    </div> \
    <div class='modal-body'> \
      <form class='form-horizontal' method='GET'> \
        <fieldset> \
        <div class='control-group'> \
          <label class='control-label' for='actor-search'>Add an Actor</label> \
          <div class='controls'> \
            <input id='actor-search' type='text' name='actors' placeholder='Type actor or actress name here...' data-provide='typeahead' /> \
          </div> \
        </div> \
        <div class='control-group'> \
        <label class='control-label' for='director-search'>Add a Director</label> \
          <div class='controls'> \
            <input id='director-search' type='text' name='directors' placeholder='Type director name here...' data-provide='typeahead' /> \
          </div> \
        </div> \
        <div class='control-group'> \
          <label class='control-label' for='genre-filter'>Filter by Genre</label> \
          <div class='controls'> \
          <% for (var i = 0; i < genres.length; i++) { %> \
            <% var genre = genres[i]; %> \
            <label class='checkbox'> \
            <input type='checkbox' name='genres' value='<%= genre.fields.url %>' /> \
            <%= genre.fields.name %> \
            </label> \
          <% } %> \
          </div> \
        </div> \
        <div class='control-group'> \
          <div class='controls'> \
        <input type='submit' value='Filter My Results' id='filter-submit' href='#' class='btn btn-large btn-primary' /> \
          </div> \
        </div> \
        </fieldset> \
      </form> \
    </div> ");
  
  // Helper functions
  var loadMovies = function(timePeriod, page, parameters) {
    var url = '/movies/' + timePeriod + '/' + page + '/?' + parameters;
    var listSelector = '#' + timePeriod + ' .thumbnails';
    $.get(url, function(movies) {
      var thumbnails = movieTemplate({ movies: movies });
      $(listSelector).append(thumbnails);
      $(listSelector).trigger('appended');
    });
  }

  var infiniteScroll = _.debounce(function() {
    var break_point = $(document).height() - ($(window).height() * 1.02);
    if ($(window).scrollTop() >= break_point) {
      var timePeriod = $('.tab-content').find('.active').attr('id');
      var nextPage = $('#'+timePeriod+' ul li:last').attr('data-next');
      if (nextPage) {
        loadMovies(timePeriod, nextPage, currentParameters);
      }
    }
  }, 250);

  // Initializer
  loadMovies('today', 1, currentParameters);
  $('#filter-options').hide();

  // Listeners 
  $('#filters a[href="#week"]').one("click", function() {
    loadMovies('week', 1, currentParameters);
  });

  $('#filters a[href="#month"]').one("click", function() {
    loadMovies('month', 1, currentParameters);
  });

  $('#filters a[href="#alltime"]').one("click", function() {
    loadMovies('alltime', 1, currentParameters);
  });

  $('#filter-settings a').one("click", function() {
    $.get('/movies/genres/all', function(genres) {
      var form = filtersTemplate({ genres: genres });
      $('#filter-options').append(form);
      $('#filter-options').trigger('appended');
    });
  });

  $('#filter-options').bind('appended', function() {
    $.get('/movies/cast/all', function(cast) {
      $('#actor-search').typeahead({ 'source': cast.actors });
      $('#director-search').typeahead({ 'source': cast.directors });
    });

    $('#filter-options').find('form').submit(function() {
      $('.thumbnails').empty();
      var timePeriod = $('.tab-content').find('.active').attr('id');
      currentParameters = $(this).serialize();
      loadMovies(timePeriod, 1, currentParameters);
      $('#filter-options').modal('toggle');
      return false;
    });
  });

  $('.thumbnails').bind('appended', function() {
    $('.tab-content').find('.active').find('.thumbnail').popover({ 'placement': 'bottom' });
  });

  $(window).scroll(infiniteScroll);
});
