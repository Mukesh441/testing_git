from flask import Flask, request, jsonify, render_template_string, redirect, url_for

app = Flask(__name__)

# In-memory storage for users and products

users = {}
products = {}

# HTML template for the combined form
combined_form_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Create User or Product</title>
</head>
<body>
    <h1>Create a New User</h1>
    <form action="{{ url_for('create_user_from_form') }}" method="POST">
        <label for="user_name">Name:</label><br>
        <input type="text" id="user_name" name="name" required><br><br>
        <label for="email">Email:</label><br>
        <input type="email" id="email" name="email" required><br><br>
        <input type="submit" value="Submit">
    </form>

    <h2>View Users</h2>
    <ul>
        {% for user_id, user in users.items() %}
            <li><a href="{{ url_for('get_user', user_id=user_id) }}">User {{ user_id }}: {{ user.name }} - {{ user.email }}</a></li>
        {% endfor %}
    </ul>

    <hr>

    <h1>Create a New Product</h1>
    <form action="{{ url_for('create_product_from_form') }}" method="POST">
        <label for="product_name">Name:</label><br>
        <input type="text" id="product_name" name="name" required><br><br>
        <label for="price">Price:</label><br>
        <input type="number" id="price" name="price" step="0.01" required><br><br>
        <input type="submit" value="Submit">
    </form>

    <h2>View Products</h2>
    <ul>
        {% for product_id, product in products.items() %}
            <li><a href="{{ url_for('get_product', product_id=product_id) }}">Product {{ product_id }}: {{ product.name }} - ${{ product.price }}</a></li>
        {% endfor %}
    </ul>
</body>
</html>
"""

# Home route to display both forms
@app.route('/')
def home():
    return render_template_string(combined_form_template, users=users, products=products)

# User service routes
@app.route('/create_user', methods=['POST'])
def create_user_from_form():
    name = request.form.get('name')
    email = request.form.get('email')
    user_id = len(users) + 1
    users[user_id] = {"name": name, "email": email}
    return redirect(url_for('home'))

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404

# Product service routes
@app.route('/create_product', methods=['POST'])
def create_product_from_form():
    name = request.form.get('name')
    price = request.form.get('price')
    product_id = len(products) + 1
    products[product_id] = {"name": name, "price": float(price)}
    return redirect(url_for('home'))

@app.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = products.get(product_id)
    if product:
        return jsonify(product), 200
    else:
        return jsonify({"error": "Product not found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
