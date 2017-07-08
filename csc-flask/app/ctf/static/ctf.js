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
    $(".challenge-selector").click(selectCTF);
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
  });
}

function selectCTF(e) {
  e.preventDefault();
  var target = $(this).attr("data-target");
  var url = $(this).attr("href")
  var resp = $.post(url + "?" + $.param({ctf: $(this).text()}), {key: $("#token").val()})
  resp.done(
    function(data) {
      $(target).hide(100);
      $(target).html(data);
      $(target).show(200);
      $("#add-flag").click(addFlag);
      $(".flag-submit").click(submitFlag);
      $(".flag-edit").click(editFlag);
    }
  );
}

function setFlagHTML(target, data) {
  $(target).hide(100);
  $(target).html(data);
  $(target).show(200);
  $("#generate").click(generateFlag);
  $(".button-clicker").click(
    function(e) {
      e.preventDefault();
      var target = $(this).attr("data-target");
      $(target).click();
    }
  );
}

function addFlag(e) {
  e.preventDefault();
  var target = $(this).attr("data-target");
  var url = $(this).attr("href")
  var resp = $.get(url, {ctf: $(this).attr("data-name")})
  resp.done(
    function(data) {
      setFlagHTML(target, data);
    }
  );
}

function submitFlag(e) {
  e.preventDefault();
  var target = $(this).attr("data-target");
  var url = $(this).attr("href")
  var resp = $.post(url + "?" + $.param({id: $(target).attr("name"), flag: $(target).val()}), {key: $("#token").val()});
  resp.done(
    function(data) {
      if(data == "") {
        $(this).prop("disabled", true);
        $(target).prop("disabled", true);
      }
    }
  );
  resp.fail(
    function(data) {
      alert("Failed");
    }
  );
}

function editFlag(e) {
  e.preventDefault();
  var target = $(this).attr("data-target");
  var url = $(this).attr("href")
  var resp = $.post(url + "?" + $.param({id: $(target).attr("name")}), {key: $("#token").val()});
  resp.done(
    function(data) {
        setFlagHTML(target, data);
    }
  );
  resp.fail(
    function(data) {
      alert("An error occurred");
    }
  );
}

function generateFlag(e) {
  e.preventDefault();
  var target = $(this).attr("data-target");
  var result = 'KEY_';
  const chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  for (var i = 20; i > 0; --i) result += chars[Math.floor(Math.random() * chars.length)];
  $(target).val(result);
}
