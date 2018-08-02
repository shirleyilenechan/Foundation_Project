function submitFavorites(evt){

    let formInputs = {
        "sku_id": evt.target.dataset.sku
    };

    $.post("/add_favorite", 
            formInputs, 
            function (result) {
                if (result.status === "ok") {
                    $(evt.target).attr("src", "https://hf-sh.org/sacredheart/wp-content/uploads/sites/3/2017/12/heart-red.png");
                }
                else if (result.status === "deleted") {
                    $(evt.target).attr("src", "http://iconshow.me/media/images/ui/iOS7-optimized-icon/png/256/39.heart.png"); 
                }
            });

}

$(".heart").on("click", submitFavorites); 


$(document).ready(function(){
    $('[data-toggle="popover"]').popover();
});