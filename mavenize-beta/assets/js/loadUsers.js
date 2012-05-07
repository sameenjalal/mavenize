(function($) {
  // Templates
  var userTemplate = _.template("\
    <% for (var i = 0; i < users.length; i++) { %>\
      <% var user = users[i]; %>\
      <li class='user-box'>\
        <div class='user-avatar pull-left'>\
          <img src='<%= user.image_url %>' width='100' height='100' />\
        </div>\
        <div class='user-content'>\
          <p class='user-name'><a href='<%= user.url %>'><%= user.full_name %></a></p>\
          <p><i><%= user.about_me %></i></p>\
          <% if (user.is_following) { %>\
            <button class='btn btn-warning'>Unfollow</button>\
          <% }\
          else { %>\
            <button class='btn btn-success'>Follow</button>\
          <% } %>\
        </div>\
    <% } %>"); 

    // Plugin
    $.fn.loadUsers = function(url) {
      listSelector = $(this);
      $.get(url, function(users) {
        var userBoxes = userTemplate({ users: users });
        $(listSelector).append(userBoxes);
        $(listSelector).trigger('appended');
      });
    }
}) (jQuery);
