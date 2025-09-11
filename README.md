# ERP Decor Tiles

This is a Django-based ERP and e-commerce platform for West Africa Decor Tiles. It supports inventory management, sales, CRM, and analytics.

## Features

*   **Product Catalog:** Browse and search for tile products.
*   **Product Details:** View detailed information about each product, including images, price, and specifications.
*   **Shopping Cart:** Add products to a shopping cart and manage the cart items.
*   **Checkout:** Place an order and provide shipping information.
*   **User Authentication:** Register and log in to the website.
*   **Order History:** View past orders.
*   **Admin Interface:** Manage products, orders, and users.

## Getting Started

To get started with this project, you will need to have Python, pip, and virtualenv installed.

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the database migrations:**
    ```bash
    python manage.py migrate
    ```
5.  **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```
6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

The application will be available at `http://127.0.0.1:8000/`.

## Project Structure

*   `myproject/`: The main Django project directory.
*   `inventory/`: The Django app for managing inventory.
*   `orders/`: The Django app for managing orders.
*   `users/`: The Django app for managing users.
*   `communications/`: The Django app for managing communications.
*   `templates/`: The templates for the website.
*   `static/`: The static files for the website.

## Testing

To run the tests, use the following command:

```bash
python manage.py test
```