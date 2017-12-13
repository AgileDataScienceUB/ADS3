(function ($, document, window) {
    $(document).ready(function () {
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
                    $("#navbar-guest").removeClass("hide-container");
                }else{
                    $("#navbar-user").removeClass("hide-container");
                    $("#navbar-username").html(data["user_name"]);
                }
            },
            type: 'GET'
        });

        $("#navbar-log-out").on('click', function () {
            $.ajax({
                url: ROOT+'api/logout/',
                crossDomain: true,
                error: function(a) {
                    alert("AJAX Error");
                    console.log(a)
                },
                dataType: 'text',
                success: function(data) {
                    window.location.reload()
                },
                type: 'GET'
            });
        });

    })
})(jQuery, document, window);