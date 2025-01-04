document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('addItemToInventoryForm').addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent the default form submission behavior
        
        const formData = new FormData(this);
        const url = this.getAttribute('data-url');  // Get the URL from the data-url attribute

        fetch(url,  {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            const messageModal = document.getElementById('messageModal');
            const messageTitle = document.getElementById('messageTitle');
            const messageContent = document.getElementById('messageContent');
            if (data.success) {
                messageTitle.innerText = 'Success';
                messageContent.innerText = 'Item successfully added to inventory!';
                messageModal.style.display = 'block';  // Display the modal
                
                // Clear the form
                document.getElementById('addItemToInventoryForm').reset();
                
                // Update the inventory table
                const table = document.getElementById('inventoryTable').getElementsByTagName('tbody')[0];
                let existingRow = document.querySelector(`tr[data-id='${data.inventory_item.id}']`);
                const barcodeUrl = `/static/barcodes/${data.inventory_item.barcode}.png`;
                if (existingRow) {
                    existingRow.cells[1].innerText = data.inventory_item.quantity;
                    existingRow.cells[2].innerText = data.inventory_item.manufacturing_date;
                    existingRow.cells[3].innerText = data.inventory_item.expiry_date;
                    existingRow.cells[4].innerHTML = `<img src="${barcodeUrl}" alt="Barcode" class="table-img-50">`;
                } else {
                    const newRow = table.insertRow(0);
                    newRow.setAttribute('data-id', data.inventory_item.id);
                    newRow.insertCell(0).innerText = data.inventory_item.unique_item.name;
                    newRow.insertCell(1).innerText = data.inventory_item.quantity;
                    newRow.insertCell(2).innerText = data.inventory_item.manufacturing_date;
                    newRow.insertCell(3).innerText = data.inventory_item.expiry_date;
                    const barcodeCell = newRow.insertCell(4);
                    barcodeCell.className = 'barcode-column-50';
                    barcodeCell.innerHTML = `<img src="${barcodeUrl}" alt="Barcode" class="table-img-50">`;
                }
            } else {
                messageTitle.innerText = 'Error';
                messageContent.innerText = 'Error adding item to inventory.';
                messageModal.style.display = 'block';  // Display the modal
            }
        })
        .catch(error => {
            const messageModal = document.getElementById('messageModal');
            const messageTitle = document.getElementById('messageTitle');
            const messageContent = document.getElementById('messageContent');
            messageTitle.innerText = 'Error';
            messageContent.innerText = 'Error adding item to inventory.';
            messageModal.style.display = 'block';  // Display the modal
            console.error('Error:', error);
        });
    });

    // Modal functionality
    var messageModal = document.getElementById('messageModal');
    var closeMessageModal = document.getElementById('closeMessageModal');
    closeMessageModal.onclick = function() {
        messageModal.style.display = 'none';
    }
    window.onclick = function(event) {
        if (event.target == messageModal) {
            messageModal.style.display = 'none';
        }
    }
});