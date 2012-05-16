$(document).ready(function () {
  // Global Variables
  var userId = window.location.pathname.match(/\d+/);

  // Helper Functions
  var getRavesUrl = function(page) {
    return '/users/' + userId + '/raves/' + page;
  }

  var getMarksUrl = function(page) {
    return '/users/' + userId + '/marks/' + page;
  }

  var getFollowingUrl = function(page) {
    return '/users/' + userId + '/following/' + page;
  }

  var getFollowersUrl = function(page) {
    return '/users/' + userId + '/followers/' + page;
  }

  var infiniteScroll = _.debounce(function() {
    var break_point = $(document).height() - ($(window).height() * 1.02);
    if ($(window).scrollTop() >= break_point) {
      var activeTab = $('.active:first a').attr('href');
      var nextPage = $('.active ul li:last').attr('data-next');
      if (nextPage) {
        if (activeTab == "#raves")
          $(activeTab + ' ul').loadActivities(getRavesUrl(nextPage));
        else if (activeTab == "#marks")
          $(activeTab + ' ul').loadMovies(getMarksUrl(nextPage));
        else if (activeTab == "#following")
          $(activeTab + ' ul').loadUsers(getFollowingUrl(nextPage));
        else if (activeTab == "#followers")
          $(activeTab + ' ul').loadUsers(getFollowersUrl(nextPage));
      }
    }
  }, 250);

  // Initializer
  $('.activities').loadActivities(getRavesUrl(1));

  // Listeners
  $('#filters a[href="#marks"]').one("click", function() {
    $('#marks .thumbnails').loadMovies(getMarksUrl(1));
  });

  $('#filters a[href="#following"]').one("click", function() {
    $('#following .users').loadUsers(getFollowingUrl(1));
  });

  $('#filters a[href="#followers"]').one("click", function() {
    $('#followers .users').loadUsers(getFollowersUrl(1));
  });

  $(window).scroll(infiniteScroll);
});
