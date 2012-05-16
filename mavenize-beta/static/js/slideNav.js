$(document).ready(function() {
  var $el, leftPos, newWidth, $mainNav = $('#filters');
  $mainNav.append('<li id="underscore"></li>');
  var $underscore = $("#underscore");
  $('#filters li:first').addClass('active');

  $underscore
    .width($('.active').width()-12)
    .css('left', $('.active a').position().left-4)
    .data('origLeft', $underscore.position().left)
    .data('origWidth', $underscore.width());

  $('#filters li a').hover(function() {
    $el = $(this)
    leftPos = $el.position().left-4;
    newWidth = $el.parent().width();
    $underscore.stop().animate({
      left: leftPos,
      width: newWidth
    });
    }, function() {
      $underscore.stop().animate({
        left: $underscore.data('origLeft'),
        width: $underscore.data('origWidth')
    });
  });

  $('#filters li a').click(function() {
    $el = $(this)
    $underscore
      .width($el.parent().width())
      .css('left', $el.position().left-4)
      .data('origLeft', $underscore.position().left)
      .data('origWidth', $underscore.width());
  });
});
