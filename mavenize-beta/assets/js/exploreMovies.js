$(document).ready(function () {
  // Global Variables
  var currentParameters = '';

  // Templates
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

  var getUrl = function(timePeriod, page) {
    return '/movies/' + timePeriod + '/' + page + '/?' + currentParameters;
  }

  var infiniteScroll = _.debounce(function() {
    var break_point = $(document).height() - ($(window).height() * 1.02);
    if ($(window).scrollTop() >= break_point) {
      var timePeriod = $('.tab-content').find('.active').attr('id');
      var nextPage = $('#'+timePeriod+' ul li:last').attr('data-next');
      if (nextPage) {
        $('.tab-content .active .thumbnails').loadMovies(
          getUrl(timePeriod, nextPage));
      }
    }
  }, 250);

  // Initializer
  $('.tab-content .active .thumbnails').loadMovies(
    getUrl('today', 1))
  $('#filter-options').hide();

  // Listeners 
  $('#filters a[href="#week"]').one("click", function() {
    $('#week .thumbnails').loadMovies(
      getUrl('week', 1))
  });

  $('#filters a[href="#month"]').one("click", function() {
    $('#month .thumbnails').loadMovies(
      getUrl('month', 1))
  });

  $('#filters a[href="#alltime"]').one("click", function() {
    $('#alltime .thumbnails').loadMovies(
      getUrl('alltime', 1))
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
      $('.tab-content .active .thumbnails').loadMovies(
        getUrl(timePeriod, 1))
      $('#filter-options').modal('toggle');
      return false;
    });
  });

  $(window).scroll(infiniteScroll);
});
