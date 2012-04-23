$(document).ready(function() {
  $('#review-rating').children().click(function() {
    $('#review-submit').val($(this).val()); 
    if ($('#review-text').val() != '' &&
        $('#review-submit').attr('disabled')) {
      $('#review-submit').removeAttr('disabled');
      $('#review-submit').removeClass('disabled');
    }
  });

  $('#review-text').keyup(function() {
    if ($(this).val() != '' && $('#review-submit').val() != 0) {
      $('#review-submit').removeAttr('disabled');
      $('#review-submit').removeClass('disabled');
    }
    else {
      $('#review-submit').attr('disabled', 'true');
      $('#review-submit').addClass('disabled');
    }
  });
});
