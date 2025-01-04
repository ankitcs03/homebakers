// This file contains JavaScript functionality for the inventory management application.
// It includes QR code scanning, form submissions, and dynamic updates to the inventory list.

document.addEventListener('DOMContentLoaded', function() {
    // Function to handle QR code scanning
    const qrScanner = document.getElementById('qr-scanner');
    if (qrScanner) {
        qrScanner.addEventListener('change', function(event) {
            const barcode = event.target.value;
            // Process the scanned barcode (e.g., mark item as sold)
            markItemAsSold(barcode);
        });
    }

    // Function to mark item as sold
    function markItemAsSold(barcode) {
        fetch(`/out_item/${barcode}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ barcode: barcode }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Item marked as sold successfully!');
                // Optionally, refresh the inventory list
                updateInventoryList();
            } else {
                alert('Error marking item as sold.');
            }
        })
        .catch(error => console.error('Error:', error));
    }

    // Function to update the inventory list dynamically
    function updateInventoryList() {
        fetch('/live_inventory')
        .then(response => response.json())
        .then(data => {
            const inventoryList = document.getElementById('inventory-list');
            inventoryList.innerHTML = ''; // Clear existing list
            data.items.forEach(item => {
                const listItem = document.createElement('li');
                listItem.textContent = `${item.name} - ${item.quantity} (Barcode: ${item.barcode})`;
                inventoryList.appendChild(listItem);
            });
        })
        .catch(error => console.error('Error fetching inventory:', error));
    }
});