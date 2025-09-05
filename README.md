# 🛒 Flask + MongoDB E-Commerce App

A full-featured **E-Commerce Web Application** built with **Flask (Python)** and **MongoDB**.  
It includes user authentication, product management, shopping cart, order tracking, payments, contact form, complaints, and an admin dashboard.

---

## 🚀 Features
- **User Authentication** (Register, Login, Logout, Hashed Passwords)
- **Product Management** (Add, View, Upload Images)
- **Shopping Cart** (Add, Update, Remove, Persistent in Session)
- **Orders** (Place & View Orders with Total Price)
- **Payments** (Record transactions with amount & method)
- **Contact Form & Complaints**
- **Admin Dashboard** to manage Products, Orders, Payments, Contacts, Complaints

---

## 📂 Project Structure
flask-mongo-ecommerce/
│-- app.py # Main Flask App
│-- requirements.txt # Python dependencies
│-- static/ # CSS, JS, Images
│-- templates/ # HTML Templates
│-- .gitignore # Git ignore rules
│-- README.md # Project documentation


---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/flask-mongo-ecommerce.git
cd flask-mongo-ecommerce

2️⃣ Create Virtual Environment & Install Dependencies
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

pip install -r requirements.txt

3️⃣ Run MongoDB

Make sure MongoDB is running locally or update the URI in app.py:

client = MongoClient("mongodb://localhost:27017/")

4️⃣ Run the Flask App
python app.py
Visit: http://127.0.0.1:5000/

🛠 Requirements

Python 3.8+

Flask

Flask-PyMongo / PyMongo

Werkzeug

MongoDB

Install with:pip install flask pymongo werkzeug

🔑 Admin Access

To access the admin dashboard:

Log in as a user with username/email marked as admin (modify in DB).

Visit /admin.

🚀 Deployment

You can deploy this app on:

Render

Heroku

PythonAnywhere

For production, use MongoDB Atlas instead of local MongoDB.


📜 License

This project is licensed under the MIT License.


