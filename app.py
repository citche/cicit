from flask import Flask, flash, jsonify, render_template, request, redirect, url_for, session
import mysql
import mysql.connector
from mysql.connector import Error
import os
from werkzeug.security import generate_password_hash, check_password_hash



connection = mysql.connector.connect(
    host='rst-db.mysql.database.azure.com',  # Replace with your Azure MySQL host
    user='adminadmin',  # Replace with your Azure MySQL username
    password='Admin123',  # Replace with your Azure MySQL password
    database='gymdb',  # Replace with your Azure MySQL database name
    port='3306'  # Ensure this path is correct
)

if connection.is_connected():
    print('Connected to MySQL Database')

def get_azure_db_connection():
    try:
        connection = mysql.connector.connect(
            host=('rst-db.mysql.database.azure.com'),
            user=('adminadmin'),
            password=('Admin123'),
            database=('gymdb'),
            port='3306'
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")
        return None

app = Flask(__name__, 
            static_folder='static', 
            template_folder='templates')
app.secret_key = ('SECRET_KEY', 'fallback_secret_key')

# # Konfigurasi database MySQL
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'db_gymrist'



# Halaman utama
@app.route('/')
def home():
    return render_template('index.html')

# Halaman about
@app.route('/about')
def about():
    return render_template('about.html')

# Halaman contact
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Halaman class
@app.route('/class', endpoint='class') 
def class_view():  
    return render_template('class.html') 

# Halaman feature
@app.route('/feature')
def feature():
    return render_template('feature.html')

# Halaman blog
@app.route('/blog')
def blog():
    return render_template('blog.html')

# Halaman single
@app.route('/single')
def single():
    return render_template('single.html')

@app.route('/jadwal')
def jadwal_view():
    return render_template('jadwal.html')

# Halaman login
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            # Get form data
            username = request.form.get('username')
            password = request.form.get('password')

            # Input validation
            if not username or not password:
                flash('Username and password are required')
                return render_template('signup.html')

            # Hash the password
            hashed_password = generate_password_hash(password)

            # Database connection
            connection = get_azure_db_connection()
            if not connection:
                flash('Database connection error')
                return render_template('signup.html'), 500

            cursor = connection.cursor(dictionary=True)

            # Check if user exists
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash('Username already exists')
                cursor.close()
                connection.close()
                return render_template('signup.html')

            # Insert new user
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)", 
                (username, hashed_password)
            )
            connection.commit()

            # Clean up
            cursor.close()
            connection.close()

            flash('Signup successful')
            return redirect(url_for('login'))

        except Exception as e:
            # Comprehensive error logging
            app.logger.error(f"Signup error: {str(e)}")
            flash(f'An error occurred: {str(e)}')
            return render_template('signup.html'), 500

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')

            # Database connection
            connection = get_azure_db_connection()
            if not connection:
                flash('Database connection error')
                return render_template('login.html'), 500

            cursor = connection.cursor(dictionary=True)

            # Verify user
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()

            cursor.close()
            connection.close()

            if user and check_password_hash(user['password'], password):
                # Successful login logic (e.g., session management)
                flash('Login successful')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password')
                return render_template('login.html')

        except Exception as e:
            app.logger.error(f"Login error: {str(e)}")
            flash(f'An error occurred: {str(e)}')
            return render_template('login.html'), 500

    return render_template('login.html')

@app.route('/admin', methods=['GET'])
def admin():
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("SELECT id, username, created_at FROM users")
        users = cursor.fetchall()  # Ambil semua data pengguna
    except Exception as e:
        flash(f"Error fetching users: {str(e)}", "danger")
        users = []
    finally:
        cursor.close()
    
    return render_template('admin.html', users=users)

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Menghapus sesi pengguna
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

@app.route('/class')
def manage_schedule():
    conn = get_azure_db_connection()
    if not conn:
        return "Database connection failed", 500
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ak")
        result = cursor.fetchall()
        return render_template('kegiatan.html', ak=result)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return f"Database error: {err}", 500
    finally:
        if conn:
            cursor.close()
            conn.close()




if __name__ == '__main__':
    app.run(debug=True)