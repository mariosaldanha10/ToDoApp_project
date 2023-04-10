from flask import Flask, render_template, request, url_for, redirect, session
import pymongo
from bson.objectid import ObjectId
import bcrypt
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

client = pymongo.MongoClient(
    'mongodb+srv://22453:Admin123@cluster0.a7d37zg.mongodb.net/?retryWrites=true&w=majority')

# database
db = client.mario_db

# collections
todos = db.todos

records = db.register


# This route checks if the user is
# logged in by checking if their email is in the session. If not, it redirects to the login page.
@app.route("/", methods=['post', 'get'])
def index():
    message = ''
    if "email" not in session:
        return redirect(url_for("login"))
    return render_template('login.html')


# REGISTER
@app.route("/registration/", methods=['post', 'get'])
def register():
    message = ''
    # Redirect to logged_in page if user already logged in
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        # Get user input
        user = request.form.get("fullname")
        email = request.form.get("email")

        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # Check if user entered a password
        if password2 is None:
            message = 'Please enter a password.'
            return render_template('registration.html', message=message)
        # Check if user or email already exists in database
        user_found = records.find_one({"name": user})
        email_found = records.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('registration.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('registration.html', message=message)
        # Check if passwords match and hash the password
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('registration.html', message=message)
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'name': user, 'email': email, 'password': hashed}
            # Insert the user data into the database
            records.insert_one(user_input)

            user_data = records.find_one({"email": email})
            new_email = user_data['email']

            return render_template('logged_in.html', email=new_email)
    return render_template('login.html')


# end of code to run it
if __name__ == "__main__":
    app.run(debug=True)


# LOGGED IN
@app.route('/logged_in')
def logged_in():
    # Checks if the email is in the session dictionary
    if "email" in session:
        # Retrieves the email from the session dictionary
        email = session["email"]
        # Renders the "logged_in" template with the email variable
        return render_template('logged_in.html', email=email)
    else:
        # Redirects the user to the login page if email is not in the session dictionary
        return redirect(url_for("login"))


# LOGIN PAGE
@app.route("/login", methods=["POST", "GET"])
def login():
    # Initialize the message variable with a default value
    message = 'Please login to your account'
    # Check if the user is already logged in, redirect to logged in page
    if "email" in session:
        return redirect(url_for("logged_in"))
    # Check if the form has been submitted via POST method
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        # Check if the entered email exists in the database
        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            # Check if the entered password matches the hashed password in the database
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('logged_in'))
            else:
                # If the password is incorrect, show an error message
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            # If the email is not found in the database, show an error message
            message = 'Email not found'
            return render_template('login.html', message=message)
        # If the form has not been submitted yet, show the login page
    return render_template('login.html', message=message)


# LOG OUT
@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)  # remove "email" from session
        return render_template("signout.html")  # render signout page
    else:
        return render_template('login.html')  # render login page

#TO-DO PAGE
@app.route('/mytodo_index/', methods=('GET', 'POST'))
def mytodo_index():
    # If form submitted
    if request.method == 'POST':
        # Get content, priority, and status from form
        content = request.form['content']
        priority = request.form['priority']
        status = request.form['status']
        # Insert to-do item into database with content, priority, and status
        todos.insert_one({'content': content, 'priority': priority, 'status': status})
        # Redirect back to to-do list page
        return redirect(url_for('mytodo_index'))
    # Get all to-do items from database
    all_todos = todos.find()
    # Render the to-do list template with the retrieved items
    return render_template('mytodo_index.html', todos=all_todos)


@app.post('/<id>/delete/')
def delete(id):
    # Delete to-do item from database with matching id
    todos.delete_one({"_id": ObjectId(id)})
    # Redirect back to to-do list page after deleting
    return redirect(url_for('mytodo_index'))
