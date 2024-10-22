document.querySelectorAll('.flash').forEach(function(flash) {
    setTimeout(function() {
        flash.remove();
    }, 5000);  
});
