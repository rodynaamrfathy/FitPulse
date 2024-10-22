document.addEventListener("DOMContentLoaded", function() {
    const rankPic = document.getElementById("rank-pic");
    const ranksModal = document.getElementById("ranksModal");
    const closeModal = document.getElementById("closeModal");

    rankPic.addEventListener("click", function() {
        ranksModal.style.display = "flex"; 
    });

    closeModal.addEventListener("click", function() {
        ranksModal.style.display = "none"; 
    });

    window.addEventListener("click", function(event) {
        if (event.target === ranksModal) {
            ranksModal.style.display = "none"; 
        }
    });
});
