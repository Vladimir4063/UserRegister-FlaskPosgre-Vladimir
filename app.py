from json import load
from flask import Flask, render_template, request, redirect, url_for, flash
from psycopg import connect
from notifypy import Notify
from dotenv import load_dotenv
from os import environ


load_dotenv()

app = Flask(__name__)

host = environ.get('DB_HOST')
port = environ.get('DB_PORT')
dbname = environ.get('DB_NAME')
user = environ.get('DB_USER')
password = environ.get('DB_PASSWORD')

notification = Notify()

def get_connection():
    conn = connect(host=host, port = port, dbname = dbname, user=user, password = password)
    return conn

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login', methods= ["GET", "POST"])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT email FROM users WHERE email = %s", (email,))
        emaildb = cur.fetchone()
        emailDbParse = parserCadena(emaildb)

        if email == emailDbParse:
            cur = conn.cursor()
            cur.execute("SELECT password FROM users WHERE password = %s and email = %s", (password, email,))
            passwordb = cur.fetchone()
            passwordbParse = parserCadena(passwordb)

            if password == passwordbParse:

                cur = conn.cursor()
                cur.execute("SELECT id_role FROM users WHERE email = %s", (email,))
                id_roledb = cur.fetchone()
                role_parse = parserInt(id_roledb)

                if role_parse == 1:
                    return render_template('admin/home-admin.html')
                if role_parse == 2:
                    return render_template('support/home-support.html')
                    
            else:
                flash('Invalid password')
                return render_template('login.html')
        else:
            flash('Invalid email')
            return render_template('login.html')
    else:
        return render_template('login.html')

def parserCadena(cadena):
    cadena = str(cadena).split(",")
    cadenaPos = cadena[0]
    cadenaParse = cadenaPos[2:-1]
    print(cadenaParse)
    return cadenaParse

def parserInt(cadena):
    cadena = str(cadena).split(",")
    cadenaPos = cadena[0]
    cadenaParse = cadenaPos[1:]
    cadenaParseInt = int(cadenaParse)
    return cadenaParseInt

@app.route('/register', methods = ["GET", "POST"])
def register():    

    if request.method == 'GET':
        return render_template("register.html")

    else:
        conn = get_connection()
        
        name = request.form['name']
        email = request.form['email']
        role = request.form['role']
        password = request.form['password']

        print(name, email, role, password)
        
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        resul = cur.fetchall()

        if len(resul) > 0:

            flash('Existing mail')
            return render_template("register.html")

        else:
            cur = conn.execute("INSERT INTO users (name, email, id_role, password) VALUES (%s, %s, %s, %s)",(name, email, role, password,))
            conn.commit()

            cur = conn.execute("SELECT * FROM users")
            resul = cur.fetchall()
            print(resul)

            cur.close()
            conn.close()
            
            return render_template("login.html")

if __name__ == '__main__':
    app.secret_key = "lallave"
    app.run(debug=True)
    