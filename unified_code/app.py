from flask import Flask, request, jsonify, render_template_string, redirect, url_for
import requests


app = Flask(__name__)


# Configuration for microservice endpoints
MICROSERVICE_URLS = {
    "user_service": "http://localhost:5001",  # Replace with actual IP and port
    "Product_details": "http:localhost:5002"
}

# HTML template for the tabbed interface
template = """
<!DOCTYPE html>
<html>
<head>
    <title>Microservices Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        .tabs {
            overflow: hidden;
            border: 1px solid #ccc;
            background-color: #f1f1f1;
        }
        .tab-button {
            background-color: #ddd;
            border: none;
            outline: none;
            cursor: pointer;
            padding: 14px 16px;
            display: inline-block;
            text-align: center;
        }
        .tab-content {
            display: none;
            padding: 20px;
            border: 1px solid #ccc;
            border-top: none;
        }
        .active-tab {
            background-color: #ccc;
        }
        .active-content {
            display: block;
        }
    </style>
</head>
<body>
    <h1>Microservices Dashboard</h1>

    <div class="tabs">
        <button class="tab-button active-tab" onclick="openTab('user_service')">user_service</button>
        <button class="tab-button" onclick="openTab('Product_details')">Product_details</button>
    </div>

    <div id="user_service" class="tab-content active-content">
        <h2>Create a New User</h2>
        <form action="{{ url_for('create_user') }}" method="POST">
            <label for="name">Name:</label><br>
            <input type="text" id="name" name="name" required><br><br>
            <label for="email">Email:</label><br>
            <input type="email" id="email" name="email" required><br><br>
            <input type="submit" value="Submit">
        </form>
        <h2>View user_service</h2>
        <ul>
            {% for user in user_service %}
                <li>{{ user.name }} ({{ user.email }})</li>
            {% endfor %}
        </ul>
    </div>

    <div id="Product_details" class="tab-content">
        <h2>Create a New Product</h2>
        <form action="{{ url_for('create_product') }}" method="POST">
            <label for="name">Name:</label><br>
            <input type="text" id="name" name="name" required><br><br>
            <label for="price">Price:</label><br>
            <input type="number" id="price" name="price" step="0.01" required><br><br>
            <input type="submit" value="Submit">
        </form>
        <h2>View Product_details</h2>
        <ul>
            {% for product in Product_details %}
                <li>{{ product.name }} - ${{ product.price }}</li>
            {% endfor %}
        </ul>
    </div>

    <script>
        function openTab(tabId) {
            var i, tabcontent, tabbuttons;
            tabcontent = document.getElementsByClassName("tab-content");
            for (i = 0; i < tabcontent.length; i++) {
                tabcontent[i].style.display = "none";  
            }
            tabbuttons = document.getElementsByClassName("tab-button");
            for (i = 0; i < tabbuttons.length; i++) {
                tabbuttons[i].className = tabbuttons[i].className.replace(" active-tab", "");
            }
            document.getElementById(tabId).style.display = "block";
            event.currentTarget.className += " active-tab";
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return redirect(url_for('view_user_service'))

@app.route('/view_user_service')
def view_user_service():
    response = requests.get(f"{MICROSERVICE_URLS['user_service']}/user_service")
    user_service = response.json() if response.status_code == 200 else []
    return render_template_string(template, user_service=user_service, Product_details=[])

@app.route('/view_Product_details')
def view_Product_details():
    response = requests.get(f"{MICROSERVICE_URLS['Product_details']}/Product_details")
    Product_details = response.json() if response.status_code == 200 else []
    return render_template_string(template, user_service=[], Product_details=Product_details)

# User Service Routes
@app.route('/create_user', methods=['POST'])
def create_user():
    user_name = request.form.get('name')
    user_email = request.form.get('email')
    response = requests.post(f"{MICROSERVICE_URLS['user_service']}/user_service", json={"name": user_name, "email": user_email})
    return redirect(url_for('view_user_service'))

# Product Service Routes
@app.route('/create_product', methods=['POST'])
def create_product():
    product_name = request.form.get('name')
    product_price = request.form.get('price')
    response = requests.post(f"{MICROSERVICE_URLS['Product_details']}/Product_details", json={"name": product_name, "price": product_price})
    return redirect(url_for('view_Product_details'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
