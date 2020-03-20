$(document).ready(function(){
  var zindex = 10;
  
  $("div.card").click(function(e){
    e.preventDefault();

    var isShowing = false;

    if ($(this).hasClass("d-card-show")) {
      isShowing = true
    }

    if ($("div.dashboard-cards").hasClass("showing")) {
      $("div.card.d-card-show")
        .removeClass("d-card-show");

      if (isShowing) {
        $("div.dashboard-cards")
          .removeClass("showing");
      } else {
        $(this)
          .css({zIndex: zindex})
          .addClass("d-card-show");

      }

      zindex++;

    } else {
      $("div.dashboard-cards")
        .addClass("showing");
      $(this)
        .css({zIndex:zindex})
        .addClass("d-card-show");

      zindex++;
    }
    
  });
});