💰 Personal Expense Tracker - Flask Web Application

A lightweight, personal, and multi-user expense tracking application built using Python Flask and the Pandas data manipulation library. This application provides a modern web interface for users to securely log and review their financial expenditures.

✨ Key Features

Multi-User Authentication: Secure user registration and login implemented using Flask-Login and Werkzeug for safe password hashing.

Personalized Dashboard: Each authenticated user accesses a private dashboard showing only their recorded expenses.

Expense Management (CRUD): Users can add new expense records and delete existing ones.

Real-Time Summary: Calculates and displays the user's total spending and provides a detailed percentage-based breakdown of expenditures by category.

Responsive Design: Features a clean, modern, and fully responsive CSS layout for optimal usability on both mobile phones and desktop browsers.

Simple Data Storage: Utilizes local CSV files (users.csv and expenses.csv) for straightforward data inspection during local development.

🚀 Local Setup and Installation

Follow these steps to get a copy of the project running on your local machine for development and testing.

Prerequisites

Python 3.8+

pip (Python package installer)

git (Version control)

Step 1: Clone the Repository

Clone the project repository to your local machine:

git clone <repository_url_here>
cd Expense_tracker


Step 2: Set Up Virtual Environment

It is highly recommended to use a virtual environment to manage dependencies:

# Create the environment
python -m venv venv

# Activate the environment (Windows)
.\venv\Scripts\activate

# Activate the environment (macOS/Linux)
source venv/bin/activate


Step 3: Install Dependencies

Install all required Python packages listed in requirements.txt:

pip install -r requirements.txt


Step 4: Run the Application

Start the Flask development server:

python app.py


The application will now be accessible in your web browser at: http://127.0.0.1:5000/

📘 Usage Instructions

Register: Navigate to the main page and click the Register link to create your new user account.

Log In: Use your username and password to access the secure dashboard.

Track Expenses: Use the "Add New Expense" form on the dashboard to input details like Date, Amount, Category, and Description.

Review: Your expenses will be immediately reflected in the "Recent Expenses" list and the "Category Breakdown" summary.

📁 Project Structure

expense_tracker/
|-- app.py               # Main Flask application and logic
|-- expenses.csv         # Stores expense data (includes user_id)
|-- users.csv            # Stores user authentication details (hashed passwords)
|-- templates/
|   |-- index.html       # Main user dashboard
|   |-- login.html       # Login form
|   |-- register.html    # Registration form
|-- static/
|   |-- style.css        # Responsive styling and design
|-- README.md            # This file
|-- requirements.txt     # Python dependencies for deployment
|-- Procfile             # Web server config for Heroku (deployment)


⚠️ Data Persistence and Deployment Warning

This application relies on local CSV files (users.csv and expenses.csv) for data storage.

This approach is NOT suitable for cloud deployment services like Render, Heroku, or Netlify Functions.

Temporary Data: When deployed on cloud platforms, data written to local files is non-persistent and will be deleted whenever the server restarts (e.g., during deployment, maintenance, or scaling).

Recommendation: For a production-ready application that requires persistent user data, the data layer must be migrated to a proper database solution like SQLite (for simple file-based data) or PostgreSQL (for full-scale web hosting).
