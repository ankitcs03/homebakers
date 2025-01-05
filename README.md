# Inventory Management Application

This is a Flask-based inventory management application that utilizes barcode scanning for efficient item management. The application allows users to add unique items, manage inventory levels, mark items as sold, and view live inventory status.

## Project Structure

```
inventory-app
├── app.py
├── templates
│   ├── add_unique_item.html
│   ├── add_item_to_inventory.html
│   ├── out_item.html
│   └── live_inventory.html
├── static
│   ├── css
│   │   └── styles.css
│   └── js
│       └── scripts.js
├── models.py
├── forms.py
├── requirements.txt
└── README.md
```

## Features

1. **Add Unique Item**: Users can add unique items with a distinct barcode.
2. **Add Item to Inventory**: Users can specify the quantity of existing unique items to add to the inventory.
3. **Mark Items as Sold**: Users can scan or select items to mark them as sold, updating the inventory accordingly.
4. **Live Inventory List**: Users can view the current inventory status, including item names, quantities, and barcodes.

## Setup Instructions

1. **Clone the Repository**:

   ```
   git clone <repository-url>
   cd inventory-app
   ```

2. **Install Dependencies**:
   It is recommended to use a virtual environment. You can create one using:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

   Then install the required packages:

   ```
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   Start the Flask application:

   ```
   python app.py
   ```

   The application will be accessible at `http://127.0.0.1:5000`.

4. ** DB Migration **:
   ```
   flask db init  # Run this only if you haven't initialized migrations before
   flask db migrate -m "Increase password_hash length"
   flask db upgrade
   ```

## Usage

- Navigate to the different pages to manage your inventory:
  - **Add Unique Item**: Add new items with unique barcodes.
  - **Add Item to Inventory**: Increase the stock of existing items.
  - **Out Item**: Mark items as sold.
  - **Live Inventory**: View the current inventory status.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
