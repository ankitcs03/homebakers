document
  .getElementById("addUniqueItemForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = new FormData(this);
    const url = this.getAttribute("data-url");

    fetch(url, {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          console.log("Hello from add_unique_item.html - suucess data");
          const table = document
            .getElementById("uniqueItemsTable")
            .getElementsByTagName("tbody")[0];
          const newRow = table.insertRow(0);
          newRow.setAttribute("data-id", data.item.id);
          newRow.insertCell(0).innerText = data.item.name;
          newRow.insertCell(1).innerText = data.item.price;
          newRow.insertCell(2).innerText = data.item.description;
          const barcodeCell = newRow.insertCell(3);
          const barcodeImg = document.createElement("img");
          barcodeImg.src = `data:image/png;base64,${data.item.barcode_image}`;
          barcodeImg.alt = "Barcode";
          barcodeImg.className = "unique-table-img";
          barcodeCell.className = "barcode-column";
          barcodeCell.appendChild(barcodeImg);
          const actionsCell = newRow.insertCell(4);
          actionsCell.className = "actions-column";
          const showButton = document.createElement("button");
          showButton.className = "action-button";
          showButton.innerText = "Show";
          showButton.onclick = function () {
            showItem(data.item.id);
          };
          actionsCell.appendChild(showButton);
          const editButton = document.createElement("button");
          editButton.className = "action-button";
          editButton.innerText = "Edit";
          editButton.onclick = function () {
            editItem(data.item.id);
          };
          actionsCell.appendChild(editButton);
          const deleteButton = document.createElement("button");
          deleteButton.className = "delete-button";
          deleteButton.innerText = "Delete";
          deleteButton.onclick = function () {
            deleteItem(data.item.id);
          };
          actionsCell.appendChild(deleteButton);

          // Clear the form
          document.getElementById("addUniqueItemForm").reset();
        } else {
          alert("Error adding item");
        }
      })
      .catch((error) => console.error("Error:", error));
  });

function showItem(itemId) {
  fetch(`/get_unique_item/${itemId}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        document.getElementById("showModalTitle").innerText = "Item Details";
        document.getElementById("detail_item_name").innerText = data.item.name;
        document.getElementById("detail_price").innerText = data.item.price;
        document.getElementById("detail_description").innerText =
          data.item.description;
        document.getElementById("detail_barcode").innerText = data.item.barcode;
        document.getElementById("showItemModal").style.display = "block";
      } else {
        alert("Error fetching item details");
      }
    })
    .catch((error) => console.error("Error:", error));
}

function editItem(itemId) {
  fetch(`/get_unique_item/${itemId}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        document.getElementById("modalTitle").innerText = "Edit Item";
        document.getElementById("modal_item_name").value = data.item.name;
        document.getElementById("modal_price").value = data.item.price;
        document.getElementById("modal_description").value =
          data.item.description;
        document.getElementById("modal_barcode").value = data.item.barcode;
        document.getElementById("editItemForm").style.display = "block";
        document.getElementById("editItemForm").onsubmit = function (event) {
          event.preventDefault();
          const formData = new FormData(this);
          fetch(`/edit_unique_item/${itemId}`, {
            method: "POST",
            body: formData,
          })
            .then((response) => response.json())
            .then((data) => {
              if (data.success) {
                const row = document.querySelector(`tr[data-id='${itemId}']`);
                row.cells[0].innerText = data.item.name;
                row.cells[1].innerText = data.item.price;
                row.cells[2].innerText = data.item.description;
                row.cells[3].querySelector(
                  "img"
                ).src = `/static/barcodes/${data.item.barcode}.png`;
                document.getElementById("itemModal").style.display = "none";
              } else {
                alert("Error editing item");
              }
            })
            .catch((error) => console.error("Error:", error));
        };
        document.getElementById("itemModal").style.display = "block";
      } else {
        alert("Error fetching item details");
      }
    })
    .catch((error) => console.error("Error:", error));
}

function deleteItem(itemId) {
  fetch(`/delete_unique_item/${itemId}`, {
    method: "DELETE",
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        const row = document.querySelector(`tr[data-id='${itemId}']`);
        row.parentNode.removeChild(row);
      } else {
        alert("Error deleting item");
      }
    })
    .catch((error) => console.error("Error:", error));
}

// Edit Modal functionality
var modal = document.getElementById("itemModal");
var span = document.getElementsByClassName("close")[0];
span.onclick = function () {
  modal.style.display = "none";
};
window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
};

// show Modal functionality
var showModal = document.getElementById("showItemModal");
var showSpan = document.getElementsByClassName("showClose")[0];
showSpan.onclick = function () {
  showModal.style.display = "none";
};
window.onclick = function (event) {
  if (event.target == modal) {
    showModal.style.display = "none";
  }
};
