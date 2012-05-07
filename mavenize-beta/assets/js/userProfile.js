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
  
});
