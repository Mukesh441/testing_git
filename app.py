from flask import Flask, request, jsonify, render_template_string, redirect, url_for

app = Flask(__name__)
#test

# In-memory product storage
products = {}

# HTML template for the form
form_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Create Product</title>
</head>
<body>
    <h1>Create a New Product</h1>
    <form action="{{ url_for('create_product_from_form') }}" method="POST">
        <label for="name">Name:</label><br>
        <input type="text" id="name" name="name" required><br><br>
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

@app.route('/')
def home():
    return render_template_string(form_template, products=products)

@app.route('/create_product', methods=['POST'])
def create_product_from_form():
    name = request.form.get('name')
    price = request.form.get('price')
    product_id = len(products) + 1
    products[product_id] = {"name": name, "price": float(price)}
    return redirect(url_for('home'))

@app.route('/Product_details/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = products.get(product_id)
    if product:
        return jsonify(product), 200
    else:
        return jsonify({"error": "Product not found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)