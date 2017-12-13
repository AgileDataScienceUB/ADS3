(function($, document, window) {

  var ROOT = window.location.protocol+'//'+window.location.host+'/';

    $.ajax({
        url: ROOT+'api/users/',
        crossDomain: true,
        error: function(a) {
            alert("AJAX Error");
            console.log(a)
        },
        dataType: 'json',
        success: function(data) {
            if(data._id === undefined){
                $("body").removeClass("hide-container");
            }else{
                window.location.replace("../");
            }
        },
        type: 'GET'
    });

    $(document).ready(function () {
        $("#register-form").on('submit',function (e) {
            e.preventDefault();

            var username = $("form#register-form #username").val().toLowerCase();

            var email = $("form#register-form #email").val().toLowerCase();
            var reEmail = $("form#register-form #re-email").val().toLowerCase();
            var emailRegex = /(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)/;

            var password = $("form#register-form #password").val();
            var rePassword = $("form#register-form #re-password").val();

            if(!emailRegex.test(email) || !emailRegex.test(reEmail)){
                alert("Input email is invalid.");
            }else if(email != reEmail){
                alert("Emails do not match.");
            }else if(password != rePassword){
                alert("Passwords do not match.");
            }else{
                data = {"user_name":username, "email":email, "password":password};
                $.ajax({
                    url:ROOT+'api/users/',
                    crossDomain: true,
                    error: function (e) {
                        alert("Ajax Error")
                    },
                    data:JSON.stringify(data),
                    dataType:'json',
                    success: function (data) {
                        if(data._id === undefined){
                            alert(data["error"])
                        }else{
                            alert("Successful registration.");
                            window.location.replace("../login/");
                        }
                    },
                    type: 'POST'
                });
            }
        });
    });

})(jQuery, document, window);