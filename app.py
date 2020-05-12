from flask import Flask , render_template, request, session, logging, url_for, redirect,flash
from flask_pymongo import PyMongo
from passlib.hash import sha256_crypt


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'klatch'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/klatch'

mongo = PyMongo(app)

#initial and register page
@app.route("/", methods=["GET", "POST"])
def index():
    
    if request.method == "POST":
        users = mongo.db.user
        preferences = mongo.db.preferences

        nom = request.form.get("nom")
        prenom = request.form.get("prenom")
        password = request.form.get("password")
        email = request.form.get("email")
        secure_password = sha256_crypt.encrypt(str(password))
        age = request.form.get("age")

        #preferences :
        musicG = request.form.get("musicG")
        hiphop = request.form.get("hiphop")
        rap = request.form.get("rap")
        raggae = request.form.get("raggae")
        swing = request.form.get("swing")
        jazz = request.form.get("jazz")
        moviesG = request.form.get("moviesG")
        comedy = request.form.get("comedy")
        romantic = request.form.get("romantic")
        scif = request.form.get("scif")
        war = request.form.get("war")
        fantazy = request.form.get("fantazy")
        documentary = request.form.get("documentary")
        western = request.form.get("western")
        history = request.form.get("history")
        psychology = request.form.get("psychology")
        politics = request.form.get("politics")
        reading = request.form.get("reading")
        languages = request.form.get("languages")
        musicalIns = request.form.get("musicalIns")
        writing = request.form.get("writing")
        sport = request.form.get("sport")
        celebrities = request.form.get("celebrities")
        science = request.form.get("science")
        theatre = request.form.get("theatre")

        users.insert({"nomuser":nom, "prenomuser":prenom, "emailuser":email, "mdp":secure_password})
        user = users.find_one({"emailuser":email})
        preferences.insert({"id":user["_id"], "Music":musicG, "Rap":rap, "Raggae":raggae, "Swing":swing, "Jazz":jazz, "Movies":moviesG, "Comedy":comedy, "Romantic":romantic, "Sci-fi":scif, "War":war, "Fantazy/Fairy tales":fantazy, "Documentary":documentary, "Western":western, "History":history, "Psychology":psychology, "Politics":politics, "Reading":reading, "Languages":languages, "Musical instruments":musicalIns, "Writing":writing, "Sport":sport, "Celebrities":celebrities, "Science and technology":science, "Theatre":theatre, "Age":age})

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