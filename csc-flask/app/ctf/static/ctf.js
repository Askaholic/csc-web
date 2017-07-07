$(document).ready(
  function() {
    $("#add-challenge").click(addCTF);

    $("#create-account").change(
      function() {
        var target = $(this).attr("data-target");
        if ($(this).is(":checked"))
          $(target).show(120);
        else
          $(target).hide(120);
      }
    );
  }
);

function addCTF(e) {
  e.preventDefault();
  var target = $(this).attr("data-target");
  var url = $(this).attr("href");
  var resp = $.get(url, function(data) {
    $(target).hide();
    $(target).html(data);
    $(target).show(120);
    $(this).hide();
    registerAddCTFFormHandlers();
  });
}

function registerAddCTFFormHandlers() {
  
}
