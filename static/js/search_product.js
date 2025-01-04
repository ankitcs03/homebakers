document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('searchProductForm').addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent the default form submission behavior
        
        const barcode = document.getElementById('barcode').value;
        
        fetch(`/get_item_by_barcode/${barcode}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('itemName').innerText = data.item.name;
                document.getElementById('itemPrice').innerText = data.item.price.toFixed(2);
                document.getElementById('manufacturingDate').innerText = data.item.manufacturing_date;
                document.getElementById('expiryDate').innerText = data.item.expiry_date;
                document.getElementById('description').innerText = data.item.description;
                document.getElementById('productDetails').style.display = 'block';
            } else {
                alert('Item not found');
                document.getElementById('productDetails').style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});