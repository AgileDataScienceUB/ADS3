(function($, document, window){

    var ROOT = window.location.protocol+'//'+window.location.host+'/';
    var user_id = false;
    var recipe_id = false;

    function deactivateLoading() {
        $(".loading").addClass("hide-container")
    }
    function showRecipe() {
        $(".recipe-container").removeClass("hide-container")
    }
    function replaceTitle(title) {
        $("#title").text(title)
    }
    function replaceImage(url) {
        $("#image").attr("src",url)
    }
    function replaceIngredients(list) {
        for (var idx in list) {
            $("#ingredients").append('<li class=\"list-group-item\">'+list[idx]+'</li>');
        }
    }

    $.ajax({
        url: ROOT+'api/users/',
        crossDomain: true,
        error: function(a) {
            console.log(a);
            window.location.reload()
        },
        dataType: 'json',
        success: function(data) {
            console.log(data);
            if(data._id !== undefined) {
                user_id = data["_id"];
            }
        },
        type: 'GET'
    });

    $(document).ready(function () {

        $.ajax({
            url: ROOT+'api/random_recipe/',
            crossDomain: true,
            error: function(a) {
                console.log(a);
                window.location.reload()
            },
            dataType: 'json',
            success: function(data) {
                console.log(data);
                if(data._id !== undefined){
                    recipe_id = data["_id"];
                    replaceTitle(data['name']);
                    replaceImage(data['image']);
                    replaceIngredients(data['list_ingredients']);
                }
            },
            type: 'GET'
        }).done(function () {
            showRecipe();
            deactivateLoading();
        });

        $('#rate').on('click',function () {
            var score = $(this).text();
            $.ajax({
                url: ROOT+'api/recipe_score/'+recipe_id+'/',
                crossDomain: true,
                error: function(a) {
                    console.log(a);
                    window.location.reload();
                },
                dataType: 'json',
                data: JSON.stringify({"rating":5}),
                success: function(data) {
                    window.location.reload();
                },
                type: 'POST'
            });
        });

        $('#next').on('click',function () {
            window.location.reload();
        });

    });

})(jQuery, document, window);