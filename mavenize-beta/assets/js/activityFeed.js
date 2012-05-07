$(document).ready(function () {
  // Helper Functions

  var getUrl = function(page) {
    return '/feed/' + page;
  }

  var infiniteScroll = _.debounce(function() {
    var break_point = $(document).height() - ($(window).height() * 1.02);
    if ($(window).scrollTop() >= break_point) {
      var nextPage = $('.active ul li:last').attr('data-next');
      if (nextPage) {
        $('.active .activities').loadActivities(getUrl(nextPage));
      }
    }
  }, 250);

  // Initializer
  $('.activities').loadActivities(getUrl(1));
  
  // Listeners
  $(window).scroll(infiniteScroll);
});
