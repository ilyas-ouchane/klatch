from flask import Flask , render_template, request, session, logging, url_for, redirect,flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


from passlib.hash import sha256_crypt
engine = create_engine("mysql+pymysql://root:@localhost/klatch")

db = scoped_session(sessionmaker(bind=engine))
app = Flask(__name__)

#page d'accueil et register
@app.route("/", methods=["GET", "POST"])
def index():
    
    if request.method == "POST":
        nom = request.form.get("nom")
        prenom = request.form.get("prenom")
        password = request.form.get("password")
        email = request.form.get("email")
        secure_password = sha256_crypt.encrypt(str(password))
        
        db.execute("INSERT INTO utilisateur(nomuser,prenomuser,emailuser,mdp) VALUES(:nom, :prenom, :email, :password)",
                                            {"nom":nom, "prenom":prenom, "email":email, "password":secure_password})
        db.commit()
        return redirect(url_for('login'))
    

    return render_template("index.html")

#login

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        emaildata = db.execute("SELECT emailuser FROM utilisateur WHERE emailuser=:email",{"email":email}).fetchone()
        passworddata = db.execute("SELECT mdp FROM utilisateur WHERE emailuser=:email",{"email":email}).fetchone()

        if emaildata is None:
            flash("No email", "danger")
            return render_template("login.html")
        
        else:
            for password_data in passworddata:
                if sha256_crypt.verify(password,password_data):
                    flash("LOGIN SUCCESSFULY", "success")
                    return redirect(url_for('profil'))
                else:
                    flash("Incorrect password","danger")
                    return render_template("login.html")



    return render_template("login.html")


if __name__ == "__main__":
    app.secret_key="klatchEnForce"
    app.run(debug=True)