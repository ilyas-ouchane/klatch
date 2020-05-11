from flask import Flask , render_template, request, session, logging, url_for, redirect,flash
from flask_pymongo import PyMongo
from passlib.hash import sha256_crypt

# engine = create_engine("mysql+pymysql://root:@localhost/klatch")

# db = scoped_session(sessionmaker(bind=engine))
app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'klatch'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/klatch'

mongo = PyMongo(app)

#page d'accueil et register
@app.route("/", methods=["GET", "POST"])
def index():
    
    if request.method == "POST":
        users = mongo.db.user
        nom = request.form.get("nom")
        prenom = request.form.get("prenom")
        password = request.form.get("password")
        email = request.form.get("email")
        secure_password = sha256_crypt.encrypt(str(password))

        users.insert({"nomuser":nom, "prenomuser":prenom, "emailuser":email, "mdp":secure_password})

        return redirect(url_for('login'))
    

    return render_template("index.html")

#login

@app.route("/login", methods=["GET","POST"])
def login():
    users = mongo.db.user
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        emaildata = users.find_one({"emailuser":email})
        #passworddata = users.find_one({"mdp":password})

        if emaildata is None:
            flash("No email", "danger")
            return render_template("login.html")
        
        else:
            # for password_data in passworddata:
                if sha256_crypt.verify(password,emaildata["mdp"]):
                    flash("LOGIN SUCCESSFULY", "success")
                    return redirect(url_for('login'))
                else:
                    flash("Incorrect password","danger")
                    return render_template("login.html")



    return render_template("login.html")


if __name__ == "__main__":
    app.secret_key="klatchEnForce"
    app.run(debug=True)