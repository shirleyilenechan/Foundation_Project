function updateReview (result){
    if (result.status === "added review") {
    $("#review_content").append($("#foundation_review").val())
    }
}
function submitReview(evt){
    evt.preventDefault(); 
    let formInputs= {
        "brandid": evt.target.dataset.brandid,
        "reviewContent": $("#foundation_review").val(), 
    };

    console.log(formInputs);

    $.post("/add_review",
            formInputs,
            updateReview); 
}

$("#submit_review").on("click", submitReview); 