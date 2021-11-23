from flask import Flask, request, render_template   #Flask Imports
import sqlite3  #database for username/passwords
import hashlib  #secure hashes and message digests
app = Flask(__name__) 
db_name = 'accounts.db'

@app.route("/")
@app.route("/login")
def main():
    return render_template("login.html")

@app.route("/login2", methods=['POST'])
def login2():
    output = request.form.to_dict()
    print(output)
    userName = output["user"]
    passWord = output["pass"]
    if request.method == 'POST':
        if verify_plain(userName, passWord):
            logSuc = 'login success'
            return render_template('home.html', logSuc = logSuc)
        else:
            invalCred = 'Invalid username/password'
            return render_template('login.html', invalCred = invalCred)
    else:
        invalMet = 'Invalid Method'
        return render_template('login.html', invalMet = invalMet)

def verify_plain(userName, passWord):
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()
    query = "SELECT PASSWORD FROM USER_PLAIN WHERE USERNAME = '{0}'".format(userName)
    c.execute(query)
    records = c.fetchone()
    conn.close()
    if not records:
        return False
    return records[0] == passWord

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/register2", methods=['POST'])
def register2():
    output = request.form.to_dict()
    print(output)
    firstName = output["fname"]
    lastName = output["lname"]
    userName = output["user"]
    passWord = output["pass"]
    missingfname = bool(firstName)
    missinglname = bool(lastName)
    missinguser = bool(userName)
    missingpass = bool(passWord)
    conn = sqlite3.connect(db_name, timeout=10)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS USER_PLAIN (USERNAME TEXT PRIMARY KEY NOT NULL, 
                                                        PASSWORD TEXT NOT NULL,
                                                        FIRST_NAME TEXT NOT NULL,
                                                        LAST_NAME TEXT NOT NULL);''')
    conn.commit()
    if (missinguser == False or missingpass == False or missingfname == False or missinglname == False):
        missing = "Missing Credentials"
        return render_template("register.html", missing = missing)
    elif verify_plain(userName, passWord):
        existing = "Username is already used"
        return render_template("register.html", existing = existing)
    else:
        c.execute("INSERT INTO USER_PLAIN (USERNAME,PASSWORD,FIRST_NAME,LAST_NAME) ""VALUES ('{0}', '{1}', '{2}', '{3}')".format(userName, passWord, firstName, lastName))
        conn.commit()
        integError = "User has been registered."
        regSuc = "Registration Success"
        return render_template("register.html", integError = integError, regSuc = regSuc)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)