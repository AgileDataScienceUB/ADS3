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
    function replaceDocumentTitle(title) {
        $("head title").text(title+" - Agile Recipe")
    }
    function generateOneRecipe(id,title,image,rating){
            var scores = '';

            if(!rating){
                scores = 'No Ratings. Be the first <span class="fa fa-check-square"></span>'
            }else{
                numberFull = Math.floor(rating);
                numberHalf = Math.ceil(rating-numberFull);
                numberEmpty = Math.floor(5-rating);

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

            var html = '<div class="recipe-container col-md-6 col-sm-12"> <a href="../../recipe/'+id+'"/"> <div class="panel panel-default"> <div class="panel-heading">'+title+'</div> <div class="panel-body" style="background: url('+image+') no-repeat center center; background-size: cover;"><span class="label label-warning label-lg"> '+scores+' </span> </div> </div> </a> </div>';
            return html;
        }
    function loadRecomanded() {
        $.ajax({
            url: ROOT+'api/recipes/',
            crossDomain: true,
            error: function(a) {
                console.log(a)
            },
            dataType: 'json',
            data:JSON.stringify({recipe_id:recipe_id}),
            success: function(data) {
                console.log(data);
                $.each(data['recipes'],function (idx) {
                    var item = data["recipes"][idx];
                    var html = generateOneRecipe(item['_id'], item['name'], item['image'], item['rating']);
                    $(".recommended").append(html);
                })
            },
            type: 'POST'
        }).done(function () {
            deactivateLoading();
        });
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
                console.log(a)
            },
            dataType: 'json',
            success: function(data) {
                console.log(data);
                if(data._id !== undefined){
                    replaceDocumentTitle(data['name']);
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
            loadRecomanded()
        });

        $('#user-rating button').on('click',function () {
            var score = $(this).text();
            $.ajax({
                url: ROOT+'api/recipe_score/'+recipe_id+'/',
                crossDomain: true,
                error: function(a) {
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