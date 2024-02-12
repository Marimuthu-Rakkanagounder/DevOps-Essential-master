from flask import Flask,redirect,url_for,render_template,request,flash,session
from sqlalchemy import create_engine, text
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import scoped_session,sessionmaker
import os

app=Flask(__name__)
app.secret_key = 'RGV2T3BzIERhc2hib2FyZAo='

engine=create_engine(f"mysql+pymysql://root:02136@db:3306/devops")
db=scoped_session(sessionmaker(bind=engine))

@app.route('/home')
@app.route('/')
def home():
    return render_template ('index.html')

########################## REGISTER FORM ####################################
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=="POST":
        username = request.form.get('uname')
        email = request.form.get('email')
        password = request.form.get('pwd')
        confirm=request.form.get('conpwd')
        password_hash = generate_password_hash(password)
        select = "SELECT email FROM register WHERE email=:email"
        emaildata = db.execute(text(select), {"email":email}).fetchone()
        
        if emaildata==None:

                if password==confirm:
                    put = "INSERT INTO register(username,email,password) VALUES(:username,:email,:password)"
                    db.execute(text(put),
                    {"username":username, "email":email, "password":password_hash})
                    db.commit()
         
                    return redirect(url_for('login'))
                else:
                    flash("password does not match","danger")
                    return redirect(url_for('index.html'))
        else:
            flash("user already existed, please login or contact admin","danger")
            return redirect(url_for('home'))
    
    return render_template('index.html')

########################## LOGIN FORM #################################
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        print(password)

        selectuser = "SELECT email FROM register WHERE email=:email"
        emaildata = db.execute(text(selectuser), {"email": email}).fetchone()
        selectpassword = "SELECT password FROM register WHERE email=:email"
        passworddata = db.execute(text(selectpassword), {"email": email}).fetchone()
        print(emaildata)
        print(passworddata)
        if emaildata is None:
            flash("No username. Can you register now? ", "danger")
            return render_template('index.html')
        else:
            if check_password_hash(passworddata[0], password):
                session['email'] = emaildata[0]  # Store email in the session
                return redirect(url_for('index'))
            else:
                flash("incorrect password", "danger")
                return render_template('index.html')

    return render_template('index.html')

#################################### PROVIDER PAGE ##########################
@app.route('/index')
def index():
    email = session.get('email')
    print(email)
    if email:
        return render_template('home.html')
    else:
        flash("You need to login first", "danger")
        return redirect(url_for('login'))

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    from gunicorn.app.base import BaseApplication
    
    class FlaskApplication(BaseApplication):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()

        def load_config(self):
            for key, value in self.options.items():
                if key in self.cfg.settings and value is not None:
                    self.cfg.set(key.lower(), value)

        def load(self):
            return self.application

    options = {
        'bind': '0.0.0.0:5000',
        'workers': 4,  # You can adjust the number of workers based on your needs
    }

    FlaskApplication(app, options).run()
