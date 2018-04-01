// Example starter JavaScript for disabling form submissions if there are invalid fields
(function() {
  'use strict';
  window.addEventListener('load', function() {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.getElementsByClassName('needs-validation');
    // Loop over them and prevent submission
    var validation = Array.prototype.filter.call(forms, function(form) {
      form.addEventListener('submit', function(event) {
        if (form.checkValidity() === false) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      }, false);
    });
  }, false);
})();

$("#email").change(function(){
    $.post("http://0.0.0.0:5000/check_email",
            {email: $(this).val()},
            function(data, status){
              var d = document.getElementById("email");
              if (status === "success"){
                if(data === "Ok"){
                  d.setCustomValidity("");
                  d.classList.remove('is-invalid');
                }else{
                  d.setCustomValidity("Already registered.");
                  d.classList.add('is-invalid');
                }

              }else{
                  // Server is unavailable...
                  // make sure we don't block the form at this stage
                  d.setCustomValidity("");
                  d.classList.remove('is-invalid');
                }
              console.log("Data: " + data + "\nStatus: " + status);
            });
});

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
