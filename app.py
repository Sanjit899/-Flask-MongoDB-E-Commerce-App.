from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ---------------- MongoDB Setup ----------------
client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI
db = client['ecommerceDB']

# Ensure upload folder exists
UPLOAD_FOLDER = 'static/images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ---------------- Authentication ----------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = db.users.find_one({"email": email})
        if user and check_password_hash(user["password"], password):
            session["user_id"] = str(user["_id"])
            session["username"] = user["name"]
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password", "danger")
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            return render_template("register.html", error="Passwords do not match")

        existing_user = db.users.find_one({"email": email})
        if existing_user:
            return render_template("register.html", error="Email already registered")

        hashed_password = generate_password_hash(password)

        db.users.insert_one({
            "name": name,
            "email": email,
            "password": hashed_password,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        flash("Registration successful! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))


# ---------------- Routes ----------------

# Home Page
@app.route('/')
def home():
    products = list(db.products.find())
    return render_template('home.html', products=products)

# About Page
@app.route('/about')
def about():
    return render_template('about.html')

# Services Page
@app.route('/services')
def services():
    return render_template('services.html')

# Products Page
@app.route('/products')
def products_page():
    products = list(db.products.find())
    for p in products:
        p['_id'] = str(p['_id'])
    return render_template('products.html', products=products)

# Add Product Page
@app.route('/add_products', methods=['GET','POST'])
def add_products():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        description = request.form['description']
        image = request.files.get('image')

        image_filename = ""
        if image and image.filename != '':
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_filename = filename

        db.products.insert_one({
            "name": name,
            "price": price,
            "description": description,
            "image": image_filename
        })
        flash("Product added successfully!")
        return redirect(url_for('add_products'))

    return render_template('add_products.html')

# ---------------- Cart ----------------

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.json
    if 'cart' not in session:
        session['cart'] = []

    for item in session['cart']:
        if item['id'] == data['id']:
            item['qty'] += data['qty']
            session.modified = True
            return jsonify({'message': f"{data['name']} quantity updated in cart!"})

    session['cart'].append(data)
    session.modified = True
    return jsonify({'message': f"{data['name']} added to cart!"})

@app.route('/cart_data')
def cart_data():
    return jsonify(session.get('cart', []))

@app.route('/update_cart', methods=['POST'])
def update_cart():
    data = request.json
    cart_items = session.get('cart', [])
    for item in cart_items:
        if item['id'] == data['id']:
            item['qty'] = max(1, int(data['qty']))
            break
    session['cart'] = cart_items
    session.modified = True
    return jsonify({'message': 'Cart updated successfully!'})

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    data = request.json
    cart_items = session.get('cart', [])
    cart_items = [item for item in cart_items if item['id'] != data['id']]
    session['cart'] = cart_items
    session.modified = True
    return jsonify({'message': 'Item removed from cart!'})

@app.route('/cart')
def cart():
    return render_template('cart.html')

# ---------------- Orders ----------------

@app.route('/place_order', methods=['POST'])
def place_order():
    cart_items = session.get('cart', [])
    if not cart_items:
        return jsonify({'message': 'Cart is empty!'}), 400

    total = sum(item['price'] * item['qty'] for item in cart_items)
    order_id = db.orders.insert_one({
        "user": session.get('username', 'Guest'),
        "products": cart_items,
        "total": total,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }).inserted_id

    session['cart'] = []
    session.modified = True
    return jsonify({'message': f'Order #{str(order_id)} placed successfully!'})

@app.route('/orders')
def orders():
    orders_list = list(db.orders.find().sort('date', -1))
    return render_template('orders.html', orders=orders_list)

# ---------------- Payment ----------------
@app.route('/payment', methods=['GET','POST'])
def payment():
    if request.method == 'POST':
        db.payments.insert_one({
            "user": request.form['user'],
            "amount": float(request.form['amount']),
            "method": request.form['method'],
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        flash("Payment successful!")
        return redirect(url_for('payment'))
    return render_template('payment.html')

# ---------------- Contact ----------------
@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        db.contacts.insert_one({
            "name": request.form['name'],
            "email": request.form['email'],
            "message": request.form['message'],
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        flash("Message sent!")
        return redirect(url_for('contact'))
    return render_template('contact.html')

# ---------------- Complaints ----------------
@app.route('/complaints', methods=['GET','POST'])
def complaints():
    if request.method == 'POST':
        db.complaints.insert_one({
            "user": request.form['user'],
            "complaint": request.form['complaint'],
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        flash("Complaint submitted!")
        return redirect(url_for('complaints'))
    return render_template('complaints.html')

# ---------------- Admin Dashboard ----------------
@app.route('/admin')
def admin():
    return render_template('admin.html',
                           products=list(db.products.find()),
                           orders=list(db.orders.find().sort('date', -1)),
                           payments=list(db.payments.find()),
                           contacts=list(db.contacts.find()),
                           complaints=list(db.complaints.find())
                          )

# ---------------- Run App ----------------
if __name__ == '__main__':
    app.run(debug=True)
