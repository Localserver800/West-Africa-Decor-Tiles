# ERP Decor Tiles - Django Project

This project is a new Django application, serving as a fresh start for the "ERP Decor Tiles" system. It aims to provide a robust backend for managing various aspects of the business, with a focus on Python and Django's capabilities.

## Project Setup

Follow these steps to set up and run the Django project locally:

1.  **Navigate to the Project Directory:**
    Open your terminal or command prompt and change to this project's directory:
    ```bash
    cd C:\Users\jonat\OneDrive\Desktop\erp-decor-tiles-1
    ```

2.  **Create a Python Virtual Environment:**
    It's highly recommended to use a virtual environment to manage project dependencies.
    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment:**
    *   **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    *   **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install Django:**
    With the virtual environment activated, install Django:
    ```bash
    pip install django
    ```

5.  **Run Database Migrations (First Time Setup):**
    After installing Django, apply the initial database migrations:
    ```bash
    python manage.py migrate
    ```

## Running the Development Server

To start the Django development server:

1.  **Ensure your virtual environment is activated** (see step 3 above).
2.  **Run the server command:**
    ```bash
    python manage.py runserver
    ```
    The server will typically run on `http://127.0.0.1:8000/`.

## Project Structure

The core Django project settings are located in the `myproject/` subdirectory.

## Note on Previous Project

This project is a new development effort, separate from the previous React and Firebase application. While the name is similar, this is a distinct codebase built with Python and Django.
