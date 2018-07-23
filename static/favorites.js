function submitFavorites(evt){

    let formInputs = {
        "sku_id": evt.target.dataset.sku
    };

    $.post("/add_favorite", 
            formInputs, 
            function (result) {
                if (result.status === "ok") {
                    $(evt.target).attr("src", "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Heart_coraz%C3%B3n.svg/1200px-Heart_coraz%C3%B3n.svg.png");
                }
                else if (result.status === "deleted") {
                    $(evt.target).attr("src", "http://www.clker.com/cliparts/3/2/2/u/b/b/white-heart-with-black-outline-md.png"); 
                }
            });

}

$(".heart").on("click", submitFavorites); 


