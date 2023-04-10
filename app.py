import secrets

import app as app
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


@app.route("/", methods=['post', 'get'])
def index():
    message = ''
    if "email" not in session:
        return redirect(url_for("login"))
    return render_template('login.html')


# register
@app.route("/registration/", methods=['post', 'get'])
def register():
    message = ''
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")

        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if password2 is None:
            message = 'Please enter a password.'
            return render_template('registration.html', message=message)

        user_found = records.find_one({"name": user})
        email_found = records.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('registration.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('registration.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('registration.html', message=message)
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'name': user, 'email': email, 'password': hashed}
            records.insert_one(user_input)

            user_data = records.find_one({"email": email})
            new_email = user_data['email']

            return render_template('logged_in.html', email=new_email)
    return render_template('login.html')


# end of code to run it
if __name__ == "__main__":
    app.run(debug=True)

    # logging in


@app.route('/logged_in')
def logged_in():
    if "email" in session:
        email = session["email"]
        return render_template('logged_in.html', email=email)
    else:
        return redirect(url_for("login"))


# login page app
@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']

            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('logged_in'))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)


# logging out
@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("signout.html")
    else:
        return render_template('login.html')


@app.route('/mytodo_index/', methods=('GET', 'POST'))
def mytodo_index():
    if request.method == 'POST':
        content = request.form['content']
        degree = request.form['degree']
        todos.insert_one({'content': content, 'degree': degree})
        return redirect(url_for('mytodo_index'))

    all_todos = todos.find()
    return render_template('mytodo_index.html', todos=all_todos)


@app.post('/<id>/delete/')
def delete(id):
    todos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('mytodo_index'))


if __name__ == '__main__':
    app.run()