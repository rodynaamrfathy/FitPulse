// Close messages automatically after 15 seconds
document.querySelectorAll('.flash').forEach(function(flash) {
    setTimeout(function() {
        flash.remove();
    }, 15000);  // 15000 ms = 15 seconds
});