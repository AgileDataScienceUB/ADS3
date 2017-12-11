(function($){
    $(document).ready(function () {

        var ROOT = 'http://0.0.0.0:5000/';

        function capitalizeFirstLetter(string) {
            return string.charAt(0).toUpperCase() + string.slice(1);
        }
        function activateLoading() {
            $(".loading").removeClass("hide-container")
        }
        function deactivateLoading() {
            $(".loading").addClass("hide-container")
        }
        function showRecipes() {
            $(".recipes-container").removeClass("hide-container")
        }
        function hideRecipes() {
            $(".recipes-container").addClass("hide-container")
        }
        function loadMoreRecipes() {
            $(".load-more .btn").html('<i class=\"fa fa-cog fa-spin fa-fw\" aria-hidden=\"true\"></i> Loading Data').attr("disabled","disabled");
            $.ajax({
                url: ROOT+'api/recipes/',
                data:JSON.stringify({"ingredients":$("#taglist").tagsinput('items')}),
                error: function() {
                    alert("AJAX error");
                },
                dataType: 'json',
                success: function(data) {
                    $.each(data['recipes'],function (idx) {
                        var item = data["recipes"][idx];
                        var html = generateOneRecipe(item['id'], item['title'], item['image'], item['score']);
                        $(".recipes").append(html);
                    })
                },
                type: 'POST'
            }).done(function () {
                $(".load-more .btn").html('Load More Recipes').removeAttr("disabled");
            });
        }
        function loadRecips() {
            ingredients = $("#taglist").tagsinput('items');
            if(ingredients.length < 1){
                hideRecipes();
                return false;
            }
            activateLoading();
            hideRecipes();
            $(".recipes").html("");
            $.ajax({
                url: ROOT+'api/recipes/',
                data:JSON.stringify({"ingredients":$("#taglist").tagsinput('items')}),
                error: function() {
                    alert("AJAX error");
                },
                dataType: 'json',
                success: function(data) {
                    $.each(data['recipes'],function (idx) {
                        var item = data["recipes"][idx];
                        var html = generateOneRecipe(item['id'], item['title'], item['image'], item['score']);
                        $(".recipes").append(html);
                    })
                },
                type: 'POST'
            }).done(function () {
                deactivateLoading();
                showRecipes();
            });
        }
        function generateOneRecipe(id,title,image,score){
            var scores = '';

            numberFull = Math.floor(score);
            numberHalf = (score-numberFull)*2;
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

            var html = '<div class="recipe-container col-md-6 col-sm-12"> <a href="recipe/'+id+'"/"> <div class="panel panel-default"> <div class="panel-heading">'+title+'</div> <div class="panel-body" style="background: url('+image+') no-repeat center center; background-size: cover;"><span class="label label-warning label-lg"> '+scores+' </span> </div> </div> </a> </div>';
            return html;
        }

        var substringMatcher = function(strs) {
            return function findMatches(q, cb) {
                var matches, substringRegex;

                // an array that will be populated with substring matches
                matches = [];

                // regex used to determine if a string contains the substring `q`
                substrRegex = new RegExp(q, 'i');

                // iterate through the pool of strings and for any string that
                // contains the substring `q`, add it to the `matches` array
                $.each(strs, function(i, str) {
                    if (substrRegex.test(str)) {
                        matches.push(capitalizeFirstLetter(str));
                    }
                });

                cb(matches);
            };
        };

        var states = ['Eggs', 'Flour', 'Oil', 'Banana', 'Apple', 'Sugar', 'Bread', 'Oranges', 'lemon', 'chicken', 'vanilla', 'thyme', 'salmon', 'cashew', 'mangos', 'salt', 'pepper', 'olive', 'garlic', 'milk', 'Cream', 'tomatoe', 'rice', 'ginger', 'honey', 'corn', 'basil', 'mint', 'bacon', 'carrot'];

        // TODO: find a better autocomplete plugin compatible with ajax
        $('#typeahead').typeahead({
                hint: true,
                highlight: true,
                minLength: 1
            },
            {
                name: 'states',
                source: substringMatcher(states) // CHANGE: load the list dynamically
            });

        $("#ingredients-form").submit(function (e) {
            e. preventDefault();
            var value = $("#typeahead", this).val();

            if(value){
                $("#taglist").tagsinput('add', capitalizeFirstLetter(value));
            }

            $("#typeahead", this).typeahead('val','');
        });

        $("#typeahead").focus();
        $("#ingredients").click(function(){
            $("#typeahead").focus();
        });

        $('#taglist').on('itemAdded', function(event) {
            loadRecips()
        });
        $('#taglist').on('itemRemoved', function(event) {
            loadRecips()
        });
        $(".load-more").click(function(){
            loadMoreRecipes()
        })

    })
})(jQuery);