from flask import Flask, request

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    if "'" in username or "--" in username:
        return "SQL Injection Detected!", 400
    if username == "admin" and password == "admin":
        return "Welcome Admin", 200
    return "Login Failed", 401

if __name__ == '__main__':
    app.run(debug=True)
