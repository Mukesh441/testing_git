from flask import Flask, request, jsonify, render_template_string, redirect, url_for


app = Flask(__name__)

# In-memory user storage
users = {}

# HTML template for the form
form_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Create User</title>
</head>
<body>
    <h1>Create a New User</h1>
    <form action="{{ url_for('create_user_from_form') }}" method="POST">
        <label for="name">Name:</label><br>
        <input type="text" id="name" name="name" required><br><br>
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
</body>
</html>
"""


@app.route('/')
def home():
    return render_template_string(form_template, users = users)

@app.route('/create_user', methods=['POST'])
def create_user_from_form():
    name = request.form.get('name')
    email = request.form.get('email')
    user_id = len(users) + 1
    users[user_id] = {"name": name, "email": email}
    return redirect(url_for('home'))

@app.route('/user_service/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
