//Sidebar menu slide event
$(document).on('click', '.menu-category > span', function() {
  $(this).next('ul').slideToggle('fast', function() {
    var icon = $(this).prev('span').children('i');

    icon.removeClass();

    $(this).is(":visible") ? icon.addClass('icon icon-minus') : icon.addClass('icon icon-plus');
  });
});