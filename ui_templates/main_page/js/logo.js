(function ($) {
    function isLogoInView()
    {
        var docViewTop = $(window).scrollTop();
        var docViewBottom = docViewTop + $(window).height();

        var elemTop = $("#logo").offset().top;
        var elemBottom = elemTop + $("#logo").height();

        return ((elemBottom <= docViewBottom) && (elemTop >= docViewTop));
    }

    $(document).ready(function () {
        $(window).on('scroll', function(){
            if(!isLogoInView()){
                $(".navbar-brand").removeClass("hide-container")
            }else{
                $(".navbar-brand").addClass("hide-container")
            }
        });
    })
})(jQuery);