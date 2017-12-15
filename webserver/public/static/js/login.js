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
        $("#login-form").on('submit',function (e) {
            e.preventDefault();
            data = {"email":$("input#email").val(), "password":$("input#password").val()};
            $.ajax({
                url:ROOT+'api/login/',
                crossDomain: true,
                error: function (e) {
                    console.log(e);
                },
                data:JSON.stringify(data),
                dataType:'json',
                success: function (data) {
                    if(data._id === undefined){
                        alert(data["error"]);
                        $("#login-form")[0].reset();
                        $("input#email").focus()
                    }else{
                        window.location.replace("../rating/message/");
                    }
                },
                type: 'POST'
            })
        })
    });

})(jQuery, document, window);