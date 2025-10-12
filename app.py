from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
from datetime import datetime
import os
import uuid # To generate unique user IDs

app = Flask(__name__)
# IMPORTANT: Set a secret key for session management and security
app.config['SECRET_KEY'] = 'your_super_secret_key_change_me!'

# --- File Names ---
EXPENSES_FILE = 'expenses.csv'
USERS_FILE = 'users.csv'
EXPENSE_HEADERS = ['id', 'user_id', 'date', 'amount', 'category', 'description']
USER_HEADERS = ['id', 'username', 'password_hash']

# --- Flask-Login Setup ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# --- User Model ---
class User(UserMixin):
    def __init__(self, id, username):
        self.id = str(id)
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    """Callback function to reload the user object from the session ID."""
    df_users = load_users_data()
    user_data = df_users[df_users['id'] == int(user_id)]
    if not user_data.empty:
        return User(id=user_data.iloc[0]['id'], username=user_data.iloc[0]['username'])
    return None

# --- Data Handlers ---

def load_data(file, headers):
    """Generic function to load a CSV file, creating it if necessary."""
    if not os.path.exists(file) or os.path.getsize(file) == 0:
        df = pd.DataFrame(columns=headers)
        df.to_csv(file, index=False)
    else:
        df = pd.read_csv(file)
    return df

def load_users_data():
    return load_data(USERS_FILE, USER_HEADERS)

def load_expenses_data():
    return load_data(EXPENSES_FILE, EXPENSE_HEADERS)

# --- Authentication Routes ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        df_users = load_users_data()
        if username in df_users['username'].values:
            flash('Username already taken. Please choose another.', 'danger')
            return render_template('register.html')

        # Get the next ID (simple auto-increment)
        new_id = df_users['id'].max() + 1 if not df_users.empty else 1
        
        new_user = pd.DataFrame([{
            'id': new_id,
            'username': username,
            'password_hash': generate_password_hash(password)
        }])
        
        new_user.to_csv(USERS_FILE, mode='a', header=False, index=False)
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        df_users = load_users_data()
        
        user_row = df_users[df_users['username'] == username]
        
        if not user_row.empty and check_password_hash(user_row.iloc[0]['password_hash'], password):
            user = User(id=user_row.iloc[0]['id'], username=username)
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# --- Expense Routes ---

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    df_expenses = load_expenses_data()
    df_expenses['user_id'] = df_expenses['user_id'].astype(str)
    # Filter expenses to only show the CURRENT USER'S data
    user_expenses = df_expenses[df_expenses['user_id'] == current_user.id].copy()
    
    # Handle the form submission (Add Expense)
    if request.method == 'POST':
        try:
            date_str = request.form['date']
            amount = float(request.form['amount'])
            category = request.form['category'].strip().capitalize()
            description = request.form['description'].strip()

            # Generate a unique ID for the expense
            expense_id = int(df_expenses['id'].max()) + 1 if not df_expenses.empty else 1

            new_expense = pd.DataFrame([{
                'id': expense_id,
                'user_id': current_user.id, # KEY CHANGE: Link to current user
                'date': date_str,
                'amount': amount,
                'category': category,
                'description': description
            }])

            # Append the new expense to the main CSV
            new_expense.to_csv(EXPENSES_FILE, mode='a', header=False, index=False)
            flash('Expense recorded successfully!', 'success')
            
        except ValueError:
            flash('Invalid input: Please ensure the amount is a valid number.', 'danger')
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')

        return redirect(url_for('index'))
    
    # Data for Summary table
    total_spent = 0
    category_summary = pd.DataFrame()
    
    if not user_expenses.empty:
        total_spent = user_expenses['amount'].sum()
        category_summary = user_expenses.groupby('category')['amount'].sum().reset_index()
        category_summary['percentage'] = (category_summary['amount'] / total_spent) * 100
        category_summary = category_summary.sort_values(by='amount', ascending=False)
    
    # Prepare data for template display
    expenses_list = user_expenses.sort_values(by='date', ascending=False).to_dict('records')

    return render_template(
        'index.html', 
        expenses=expenses_list, 
        total=f"{total_spent:,.2f}",
        summary=category_summary.to_dict('records'),
        current_date=datetime.now().strftime('%Y-%m-%d')
    )

@app.route('/delete/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    df_expenses = load_expenses_data()
    
    # Find the expense and ensure it belongs to the current user
    expense_to_delete = df_expenses[(df_expenses['id'] == expense_id) & (df_expenses['user_id'] == current_user.id)]

    if not expense_to_delete.empty:
        # Filter out the expense to be deleted
        df_expenses = df_expenses[df_expenses['id'] != expense_id]
        
        # Save the updated DataFrame back to the CSV, overwriting the old file
        df_expenses.to_csv(EXPENSES_FILE, index=False)
        flash('Expense deleted successfully!', 'success')
    else:
        flash('Expense not found or you do not have permission to delete it.', 'danger')

    return redirect(url_for('index'))

if __name__ == '__main__':
    # Ensure data files are created on first run
    load_users_data()
    load_expenses_data()
    # Note: Flask's debug mode can cause issues with session management in some environments.
    app.run(debug=True)