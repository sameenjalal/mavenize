(function($) {
  // Templates
  var userTemplate = _.template("\
    <% for (var i = 0; i < users.length; i++) { %>\
      <% var user = users[i]; %>\
      <li class='user-box' data-next='<%= user.next %>'>\
        <div class='user-avatar pull-left'>\
          <img src='<%= user.image_url %>' width='100' height='100' />\
        </div>\
        <div class='user-content'>\
          <p class='user-name'><a href='<%= user.url %>'><%= user.full_name %></a></p>\
          <p><i><%= user.about_me %></i></p>\
          <% if (user.is_following) { %>\
            <button class='btn btn-warning btn-follow' value='<%= user.id %>'>Unfollow</button>\
          <% }\
          else { %>\
            <button class='btn btn-success btn-follow' value='<%= user.id %>'>Follow</button>\
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

      $('.users').bind('appended', function() {
        $('.btn-follow').click(function() {
          var button = $(this);
          if (button.text() == 'Follow') {
            $.ajax({
              type: 'POST',
              url: '/follow/' + button.val() + '/',
              data: { csrfmiddlewaretoken: CSRF_TOKEN },
              success: function() {
                button.toggleClass('btn-follow').toggleClass('btn-unfollow');
                button.toggleClass('btn-warning').toggleClass('btn-success');
                button.text('Unfollow');
              }
            });
          }
          else {
            $.ajax({
              type: 'DELETE',
              url: '/unfollow/' + button.val() +'/',
              data: { csrfmiddlewaretoken: CSRF_TOKEN },
              success: function() {
                button.toggleClass('btn-follow').toggleClass('btn-unfollow');
                button.toggleClass('btn-warning').toggleClass('btn-success');
                button.text('Follow');
              }
            });
          }
        });
      });
    }
}) (jQuery);
