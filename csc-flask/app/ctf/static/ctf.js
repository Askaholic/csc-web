$(document).ready(
  function() {
    $("#add-challenge").click(addCTF);
    
    $("#create-account").change(
      function() {
        target = $(this).attr("data-target");
        if ($(this).is(":checked"))
          $(target).show(120);
        else
          $(target).hide(120);
      }
    );
  }
);

function addCTF() {
  alert("Clicked");
}
