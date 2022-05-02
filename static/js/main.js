const postPanel = $('#post-panel');
const likesPanel = $('#likes-panel');
const logOutPanel = $('#logout-panel');

//click function to handle the active class for profile navigation
$('li').click(function() {
    $('.active').removeClass('active');
    $(this).addClass('active');
});

//onclick events to handle which panel is showing per click
$('#post-nav-button').click(function(){
    postPanel.show();
    likesPanel.hide();
    logOutPanel.hide();
    return false;
});

$('#likes-nav-button').click(function(){
    postPanel.hide();
    logOutPanel.hide();
    likesPanel.show();
    return false;
});

$('#logout-nav-button').click(function(){
    postPanel.hide();
    likesPanel.hide();
    logOutPanel.show();
    return false;
});

// click handler for bootstraps modal
$('#deleteModal').on('shown.bs.modal', function () {
    $('#deleteModal').trigger('focus')
  });

$(document).ready(function(){
    $('.toast').toast('show');
})