$(document).ready(function() {
  /* Requires jQuery Forms (jquery.forms.js) and Rating Form
     (ratingForm.js)
   */
  var selectedReview;
  $('.modal').hide();

  // Helper Functions
  var createHeader = function(modalElement, header) {
    $(modalElement).append($('<div/>', { class: "modal-header" }));
    $(modalElement).find('.modal-header').append(
        $('<a/>', { class: "close", "data-dismiss": "modal"}).text('×'));
    $(modalElement).find('.modal-header').append(
        $('<h3/>').text(header));
  };

  var createTextArea = function(placeholder) {
    return $('<textarea>', {
      "id": "modal-text", "placeholder": placeholder, "rows": "1",
      "name": "text"
    });
  }

  var createRaveButtons = function() {
    var ratingGroup = $('<div/>', { 
        "class": "btn-group",
        "id": "modal-rating",
        "data-toggle": "buttons-radio"
    });
    for (var i = 1; i < 5; i++) {
      ratingGroup.append(
        $('<button/>', {
            "class": "btn",
            "type": "button",
            "name": "rating",
            "value": i 
        }).append($('<img/>', {"src": STATIC_URL + "img/" + i + "s.png" })));
    }
    var submitButton = $('<button/>', { 
        "class": "btn btn-large btn-primary disabled",
        "id": "modal-submit",
        "type": "submit",
        "name": "rating",
        "value": "0",
        "disabled": "true"
    }).text("Rave");

    return $(ratingGroup).after(submitButton).after(
      $('<div/>', { "style": "clear: both;" }));
  }

  // Listeners
  $('.activities').bind('appended', function() {
    $('div[class$="meta"] a').click(function() {
      selectedReview = $(this).closest('.activity').val() |
                       $(this).closest('.review').val();
    });
  });

  $('#disagree').on('show', function() {
    createHeader(this, 'Leave your own rave.');
    
    $(this).append($('<div/>', { "class": "modal-body" }));
    $(this).find('.modal-body').append($('<form/>',{
        "class": "form-horizontal",
        "action": "/disagree/" + selectedReview + "/",
        "method": "POST" 
    }));
    $(this).find('form').append(CSRF_TOKEN);
    $(this).find('form').append(
      createTextArea("Tell us what you thought, choose a rating, and rave!"));
    $('#modal-text').elastic();
    $(this).find('form').append(createRaveButtons());
    $(this).find('form').ajaxForm();
    $(this).find('form').ratingForm();
  });

  $('#thank').on('show', function() {
    createHeader(this, 'Leave a thank you note (optional).');

    $(this).append($('<div/>', { class: "modal-body" }));
    $(this).find('.modal-body').append($('<form/>', {
        "class": "form-horizontal",
        "action": "/thank/" + selectedReview + "/",
        "method": "POST" 
    }));
    $(this).find('form').append(CSRF_TOKEN);
    $(this).find('form').append(
      createTextArea("You're awesome because..."));
    $('#modal-text').elastic();

    $(this).find('form').append($('<button/>', { 
        "class": "btn btn-large btn-primary",
        "id": "modal-submit",
        "type": "submit",
        "name": "submit" 
    }).text('Thank'));
    $(this).find('form').ajaxForm();
  });

  $('.modal').on('hide', function() {
    $(this).empty();
  });
});
