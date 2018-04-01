$("input").keyup(function() {
  var target = $("#" + $(this).attr("id") + "-s");
  target.text($(this).val());
  target.css("font-size", "100%");
  var badge = $("#badge");
  var scale = badge.width() / target.width();
  if (scale < 1) target.css("font-size", (scale * 100).toString() + "%");
});
$("#local").change(function() {
  $("#lname-s, #sname-s").toggleClass("local");
});
const load_params = function() {
  const searchParams = new URLSearchParams(window.location.search);
  const keys = ["lname", "sname", "affili", "pronoun"];
  if (
    keys.reduce(
      (accumulator, currentValue) =>
        accumulator || searchParams.has(currentValue),
      false
    )
  )
    keys.forEach(function(currentValue) {
      $("#" + currentValue).val(
        searchParams.has(currentValue) ? searchParams.get(currentValue) : ""
      );
    });
  ["event", "location"].forEach(function(currentValue) {
    if (searchParams.has(currentValue))
      $("#" + currentValue).val(searchParams.get(currentValue));
  });
  if (searchParams.get("local")) {
    $("#local").prop("checked", true);
    $("#local").change();
  }
};
load_params();
$("input").keyup();