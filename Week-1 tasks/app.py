from flask import Flask, render_template, request, redirect, url_for
import secrets
import string
import random

app = Flask(__name__)

def gen_pass(length, n_uppercase, n_lowercase, n_digits, n_special):
    # Define the character sets
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digit = string.digits
    special = string.punctuation
    
    # Ensure the total number of specified characters equals the length of the password
    combination = n_uppercase + n_lowercase + n_digits + n_special
    if combination != length:
        raise ValueError("The combination must match the password length.")

    # Generate the specified number of each type of character
    password_chars = (
        [secrets.choice(uppercase) for _ in range(n_uppercase)] +
        [secrets.choice(lowercase) for _ in range(n_lowercase)] +
        [secrets.choice(digit) for _ in range(n_digits)] +
        [secrets.choice(special) for _ in range(n_special)]
    )

    # Shuffle the list to jumble the characters
    random.shuffle(password_chars)

    # Join the list into a single string
    password = ''.join(password_chars)
    
    return password

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        try:
            length = int(request.form['length'])
            n_uppercase = int(request.form['n_uppercase'])
            n_lowercase = int(request.form['n_lowercase'])
            n_digits = int(request.form['n_digits'])
            n_special = int(request.form['n_special'])
            
            # Ensure a minimum length for the password for security reasons
            if length < 8:
                raise ValueError("Password length should be at least \n 8 characters for security reasons.")
            
            password = gen_pass(length, n_uppercase, n_lowercase, n_digits, n_special)
            return redirect(url_for('display_password', password=password))
        except ValueError as e:
            error = str(e)
    return render_template('index.html', error=error)

@app.route('/password')
def display_password():
    password = request.args.get('password')
    return render_template('password.html', password=password)

if __name__ == '__main__':
    app.run(debug=True)
