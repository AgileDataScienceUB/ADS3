(function($){
    $(document).ready(function () {

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
                        matches.push(str);
                    }
                });

                cb(matches);
            };
        };

        var states = ['Eggs', 'Flour', 'Oil', 'Banana', 'Apple', 'Sugar', 'Bread', 'Oranges'];

        $('#typeahead').typeahead({
                hint: true,
                highlight: true,
                minLength: 2
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
            activateLoading()
            hideRecipes()
        });
        $('#taglist').on('itemRemoved', function(event) {
            deactivateLoading()
            showRecipes()
        });
        $(".load-more").click(function(){
            loadMoreRecipes()
        })

    })
})(jQuery);