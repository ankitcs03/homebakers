document.addEventListener('DOMContentLoaded', function() {
    const table = document.getElementById('inventoryTable');
    const printModal = document.getElementById('printModal');
    const closePrintModal = document.getElementById('closePrintModal');
    const printForm = document.getElementById('printForm');
    const selectedBarcodeInput = document.getElementById('selectedBarcode');
    const previewButton = document.getElementById('previewButton');
    const previewModal = document.getElementById('previewModal');
    const closePreviewModal = document.getElementById('closePreviewModal');
    const previewFrame = document.getElementById('previewFrame');
    const downloadButton = document.getElementById('downloadButton');

    table.addEventListener('click', function(event) {
        const row = event.target.closest('tr');
        if (row) {
            const barcode = row.getAttribute('data-barcode');
            selectedBarcodeInput.value = barcode;
            printModal.style.display = 'block';
        }
    });

    closePrintModal.onclick = function() {
        printModal.style.display = 'none';
    };

    window.onclick = function(event) {
        if (event.target == printModal) {
            printModal.style.display = 'none';
        }
        if (event.target == previewModal) {
            previewModal.style.display = 'none';
        }
    };

    previewButton.onclick = function() {
        const formData = new FormData(printForm);
        const url = '/generate_pdf?preview=true';
        fetch(url, {
            method: 'POST',
            body: formData
        })
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            previewFrame.src = url;
            previewModal.style.display = 'block';
        })
        .catch(error => console.error('Error:', error));
    };

    closePreviewModal.onclick = function() {
        previewModal.style.display = 'none';
    };

    downloadButton.onclick = function() {
        const formData = new FormData(printForm);
        const url = '/generate_pdf';
        fetch(url, {
            method: 'POST',
            body: formData
        })
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = 'codes.pdf';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        })
        .catch(error => console.error('Error:', error));
    };
});

document.getElementById('codeType').addEventListener('change', function() {
    var numCopies = document.getElementById('numCopies');
    var numCopiesLabel = document.getElementById('numCopiesLabel');
    if (this.value === 'detailslip') {
        numCopies.min = 2;
        numCopies.step = 2;
        numCopies.max = 6;
        numCopiesLabel.textContent = 'Number of Copies (multiple of 2, max 6):';
    } else {
        numCopies.min = 4;
        numCopies.step = 4;
        numCopies.max = 40;
        numCopiesLabel.textContent = 'Number of Copies (multiple of 4, max 40):';
    }
});