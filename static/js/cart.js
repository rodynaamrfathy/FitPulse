document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.quantity-button-plus').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault(); 
            const productId = this.getAttribute('data-product-id');

            fetch(`/increase_quantity/${productId}`, {
                method: 'POST'
            }).then(response => {
                if (response.ok) {
                    location.reload(); 
                } else {
                    console.error('Failed to increase quantity:', response.statusText);
                    alert('Error increasing quantity. Please try again.');
                }
            }).catch(error => {
                console.error('Error:', error);
            });
        });
    });

    document.querySelectorAll('.quantity-button-minus').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault(); 
            const productId = this.getAttribute('data-product-id');

            fetch(`/decrease_quantity/${productId}`, {
                method: 'POST'
            }).then(response => {
                if (response.ok) {
                    location.reload(); 
                } else {
                    console.error('Failed to decrease quantity:', response.statusText);
                    alert('Error decreasing quantity. Please try again.');
                }
            }).catch(error => {
                console.error('Error:', error);
            });
        });
    });
});