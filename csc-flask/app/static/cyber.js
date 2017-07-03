$(document).ready(
  function() {
    registerHandlers()
  }
);

function registerHandlers() {
  registerCheckboxHandler()
}

function registerCheckboxHandler() {
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
