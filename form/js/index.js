var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};
var backend = getUrlParameter('backend');
var secret  = getUrlParameter('secret');

$(function(){
  // Disable the form if the required info about backend server is missing
  if((backend === undefined) || (secret === undefined)){
    $("#main_form :input").prop('disabled', true);
    $('#backendModal').modal({show: true});
  }
  $("#main_form").attr('action', backend+'/register');
  $("#secret").attr('value', secret);
});

$("#email").change(function(){
    $.post(backend+"/check_email",
            {email: $(this).val(),
             secret: secret},
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
