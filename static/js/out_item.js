document.addEventListener('DOMContentLoaded', function() {
    const basket = [];
    const basketTable = document.getElementById('basketTable').getElementsByTagName('tbody')[0];
    const totalPriceElement = document.getElementById('totalPrice');
    const availableQuantityElement = document.getElementById('availableQuantity');
    let availableQuantity = 0;

    document.getElementById('barcode').addEventListener('change', function() {
        const barcode = this.value;
        
        fetch(`/get_item_by_barcode/${barcode}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                availableQuantity = data.item.quantity;
                availableQuantityElement.innerText = `Available Quantity: ${availableQuantity}`;
                document.getElementById('quantity').max = availableQuantity;
            } else {
                availableQuantityElement.innerText = 'Item not found';
                availableQuantity = 0;
                document.getElementById('quantity').max = 1;
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    document.getElementById('non-sale').addEventListener('change', function() {
        document.getElementById('descriptionField').style.display = 'block';
    });

    document.getElementById('sale').addEventListener('change', function() {
        document.getElementById('descriptionField').style.display = 'none';
    });

    document.getElementById('outItemForm').addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent the default form submission behavior
        
        const barcode = document.getElementById('barcode').value;
        const quantity = parseInt(document.getElementById('quantity').value);
        const type = document.querySelector('input[name="type"]:checked').value;
        const description = document.getElementById('description').value;
        
        if (quantity > availableQuantity) {
            alert('Quantity exceeds available inventory');
            return;
        }
        
        fetch(`/get_item_by_barcode/${barcode}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const item = data.item;
                const total = item.price * quantity;
                
                // Add item to basket
                basket.push({ ...item, quantity, total, type, description });
                
                // Update basket table
                const newRow = basketTable.insertRow();
                newRow.insertCell(0).innerText = item.name;
                newRow.insertCell(1).innerText = item.barcode;
                newRow.insertCell(2).innerText = quantity;
                newRow.insertCell(3).innerText = `$${item.price.toFixed(2)}`;
                newRow.insertCell(4).innerText = `$${total.toFixed(2)}`;
                newRow.insertCell(5).innerText = type;
                newRow.insertCell(6).innerText = description;
                
                // Update total price
                const totalPrice = basket.reduce((sum, item) => sum + item.total, 0);
                totalPriceElement.innerText = totalPrice.toFixed(2);
                
                // Clear form
                document.getElementById('outItemForm').reset();
                availableQuantityElement.innerText = '';
                document.getElementById('descriptionField').style.display = 'none';
            } else {
                console.error('Error fetching item:', data);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    document.getElementById('checkoutButton').addEventListener('click', function() {
        fetch('/checkout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(basket)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Clear basket
                basket.length = 0;
                basketTable.innerHTML = '';
                totalPriceElement.innerText = '0.00';
                alert('Checkout successful!');
            } else {
                console.error('Error during checkout:', data);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});