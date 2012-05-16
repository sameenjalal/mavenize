(function($) {
  $.fn.ratingForm = function() {

    if ($(this).has('div[id$="rating"]')) {
      ratingForm = $(this);
      submitButton = ratingForm.find('button[type="submit"]');

      // Enables submit on selection of rating if text area is not blank.
      ratingForm.find('button[type="button"]').click(function() {
        submitButton.val($(this).val());
        if (ratingForm.find('textarea').val() != '' &&
            submitButton.attr('disabled')) {
          submitButton.removeAttr('disabled').removeClass('disabled');
        }
      });

      // Enables submit on entry into the text area if rating is set.
      ratingForm.find('textarea').keyup(function() {
        if ($(this).val() != '' && submitButton.val() != 0) {
          submitButton.removeAttr('disabled').removeClass('disabled');
        }
        else {
          submitButton.attr('disabled', 'true').addClass('disabled');
        }
      });
    }
  }
}) (jQuery);
