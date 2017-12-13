(function($, document, window){

    var ROOT = window.location.protocol+'//'+window.location.host+'/';
    var urlRegex = /recipe\/([\d\w]+)/i;
    var recipe_id = urlRegex.exec(window.location.pathname)[1];
    var user_id = false;

    function deactivateLoading() {
        $(".loading").addClass("hide-container")
    }
    function showRecipe() {
        $(".recipe-container").removeClass("hide-container")
    }
    function showUserRating() {
        $("#user-rating").removeClass("hide-container")
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
    function replaceEnergy(number) {
        $("#energy").text(number+'K');
    }
    function replaceSource(url) {
        $("#source").attr("href",url)
    }
    function replaceRating(score) {
        var scores = '';

        if(!score){
            scores = 'No Ratings. Be the first <span class="fa fa-check-square"></span>'
        }else{
            numberFull = Math.floor(score);
            numberHalf = Math.ceil(score-numberFull);
            numberEmpty = Math.floor(5-score);

            for(i=0;i<numberFull;i++){
                scores += '<span class="fa fa-star"></span> '
            }
            for(i=0;i<numberHalf;i++){
                scores += '<span class="fa fa-star-half-o"></span> '
            }
            for(i=0;i<numberEmpty;i++){
                scores += '<span class="fa fa-star-o"></span> '
            }
        }

        $('#rating').html(scores);
        return true;
    }
    function replaceUserRating(score) {
        if(!score){
            return true;
        }
        $('#user-rating button:contains('+score+')').addClass("btn-success")
        $('#user-rating :not(button:contains('+score+'))').removeClass("btn-success")
    }

    $.ajax({
        url: ROOT+'api/users/',
        crossDomain: true,
        error: function(a) {
            alert("AJAX Error");
            console.log(a)
        },
        dataType: 'json',
        success: function(data) {
            console.log(data);
            if(data._id !== undefined) {
                user_id = data["_id"];
                showUserRating();
            }
        },
        type: 'GET'
    });

    $(document).ready(function () {

        $.ajax({
            url: ROOT+'api/recipes/'+recipe_id,
            crossDomain: true,
            error: function(a) {
                alert("AJAX Error");
                console.log(a)
            },
            dataType: 'json',
            success: function(data) {
                console.log(data);
                if(data._id !== undefined){
                    replaceTitle(data['name']);
                    replaceImage(data['image']);
                    replaceIngredients(data['list_ingredients']);
                    replaceEnergy(data["energy_KCal"]);
                    replaceSource(data["url"]);
                    replaceRating(data["rating"]);
                    replaceUserRating(data["user_rating"])
                }
            },
            type: 'GET'
        }).done(function () {
            showRecipe();
            deactivateLoading();
        });

        $('#user-rating button').on('click',function () {
            var score = $(this).text();
            $.ajax({
                url: ROOT+'api/recipe_score/'+recipe_id+'/',
                crossDomain: true,
                error: function(a) {
                    alert("AJAX Error");
                    console.log(a)
                },
                dataType: 'json',
                data: JSON.stringify({"rating":score}),
                success: function(data) {
                    if(data._id !== undefined) {
                        replaceUserRating(data["user_rating"]);
                        replaceRating(data["rating"])
                    }
                },
                type: 'POST'
            });
        });

    });

})(jQuery, document, window);