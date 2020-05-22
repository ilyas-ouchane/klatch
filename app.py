from flask import Flask , render_template, request, session, logging, url_for, redirect,flash
from flask_pymongo import PyMongo
from passlib.hash import sha256_crypt
from sklearn import svm
from sklearn import metrics
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'klatch'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/klatch'

mongo = PyMongo(app)
#source
@app.route("/source")
def source():
    return render_template('source.html')
#index page
@app.route("/")
def index():
    chatrooms = mongo.db.chatroom
    crPreferences = mongo.db.chatroompreferences
    nomsChatrooms = chatrooms.find({}, {'nomchatroom': 1, 'description':1})
    preferencesChatrooms = crPreferences.find({}, {"Music":1, "Rap":1, "Raggae":1, "Swing":1, "Jazz":1, "Movies":1, "Comedy":1, "Romantic":1, "Sci-fi":1, "War":1, "Fantazy/Fairy tales":1, "Documentary":1, "Western":1, "History":1, "Psychology":1, "Politics":1, "Reading":1, "Languages":1, "Musical instruments":1, "Writing":1, "Sport":1, "Celebrities":1, "Science and technology":1, "Theatre":1})
    preferencesTab = ["Music", "Rap", "Raggae", "Swing", "Jazz", "Movies", "Comedy", "Romantic", "Sci-fi", "War", "Fantazy/Fairy tales", "Documentary", "Western", "History", "Psychology", "Politics", "Reading", "Languages", "Musical instruments", "Writing", "Sport", "Celebrities", "Science and technology", "Theatre"]
    return render_template('index.html', nomsChatrooms=nomsChatrooms, preferencesChatrooms=preferencesChatrooms, preferencesTab=preferencesTab)
#profile
@app.route("/profile")
def profile():
    return render_template('profile.html')

#admin
@app.route("/admin")
def admin():
    chatrooms = mongo.db.chatroom
    crPreferences = mongo.db.chatroompreferences
    nomsChatrooms = chatrooms.find({}, {'nomchatroom': 1, 'description':1})
    preferencesChatrooms = crPreferences.find({}, {"Music":1, "Rap":1, "Raggae":1, "Swing":1, "Jazz":1, "Movies":1, "Comedy":1, "Romantic":1, "Sci-fi":1, "War":1, "Fantazy/Fairy tales":1, "Documentary":1, "Western":1, "History":1, "Psychology":1, "Politics":1, "Reading":1, "Languages":1, "Musical instruments":1, "Writing":1, "Sport":1, "Celebrities":1, "Science and technology":1, "Theatre":1})
    preferencesTab = ["Music", "Rap", "Raggae", "Swing", "Jazz", "Movies", "Comedy", "Romantic", "Sci-fi", "War", "Fantazy/Fairy tales", "Documentary", "Western", "History", "Psychology", "Politics", "Reading", "Languages", "Musical instruments", "Writing", "Sport", "Celebrities", "Science and technology", "Theatre"]
    return render_template('admin.html', nomsChatrooms=nomsChatrooms, preferencesChatrooms=preferencesChatrooms, preferencesTab=preferencesTab)

#delete chatroom
@app.route("/deletecr", methods=["GET", "POST"])
def deletecr():
    if request.method == "POST":
        chatrooms = mongo.db.chatroom
        nomcr = request.form.get("nomcr")
        chatrooms.remove({'nomchatroom': nomcr})

        return render_template('admin.html')

    return render_template('admin.html')
#register page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        users = mongo.db.user
        preferences = mongo.db.preferences

        nom = request.form.get("nom")
        prenom = request.form.get("prenom")
        password = request.form.get("password")
        email = request.form.get("email")
        secure_password = sha256_crypt.encrypt(str(password))
        age = request.form.get("age")
        genre = request.form.get("genre")

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
        preferences.insert({"id":user["_id"], "Music":musicG, "Rap":rap, "Raggae":raggae, "Swing":swing, "Jazz":jazz, "Movies":moviesG, "Comedy":comedy, "Romantic":romantic, "Sci-fi":scif, "War":war, "Fantazy/Fairy tales":fantazy, "Documentary":documentary, 
        "Western":western, "History":history, "Psychology":psychology, "Politics":politics, "Reading":reading, "Languages":languages, "Musical instruments":musicalIns, "Writing":writing, "Sport":sport, "Celebrities":celebrities, "Science and technology":science, 
        "Theatre":theatre, "Age":age, "genre": genre})

        ######################## Testing the model##########################################
        list=[musicG,hiphop,rap,raggae,swing,jazz,moviesG,comedy,romantic,scif,war,fantazy,documentary,western,history,psychology,
        politics,reading,languages,musicalIns,writing,sport,celebrities,science,theatre,age,genre]

        def test_model(list):
            #     pickle.dump(clf, open(fn, 'wb'))
            filename = 'final_model_klatch.sav'
            loaded_model = pickle.load(open(filename, 'rb'))
            A = np.array([list])
            B = A.reshape(1,-1)
            result = loaded_model.predict(B)
            return(result[0])

        chatroom_recommended_id = test_model(list)
        ###########################################################
        ## Now we need to find a way to : 
                 ## Display the recommended chat-room that has the ID of recommended_chatroom_id  
                 ## in another page --> redirect to it 
                 ## Register the user 
        ###########################################################



        return render_template("list.html", chatroom_recommended_id=chatroom_recommended_id)
    return render_template("register.html")

#list

@app.route("/list")
def list():
    return render_template("list.html")
#register page
@app.route("/create_chatroom", methods=["GET", "POST"])
def create_chatroom():
    if request.method == "POST":
        chatrooms = mongo.db.chatroom
        chatroompreferences = mongo.db.chatroompreferences
        #chatroom_info
        nomcr = request.form.get("nomcr")
        descr = request.form.get("descr")       
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

        chatrooms.insert({"nomchatroom":nomcr, "description":descr})
        session['chatroom'] = nomcr
        chatroom = chatrooms.find_one({"nomchatroom":nomcr})
        chatroompreferences.insert({"id":chatroom["_id"], "Music":musicG, "Rap":rap, "Raggae":raggae, "Swing":swing, "Jazz":jazz, "Movies":moviesG, "Comedy":comedy, "Romantic":romantic, "Sci-fi":scif, "War":war, "Fantazy/Fairy tales":fantazy, "Documentary":documentary, "Western":western, "History":history, "Psychology":psychology, "Politics":politics, "Reading":reading, "Languages":languages, "Musical instruments":musicalIns, "Writing":writing, "Sport":sport, "Celebrities":celebrities, "Science and technology":science, "Theatre":theatre})

        return redirect('http://localhost:3000', code=301)
    return render_template("create_chatroom.html")    

#login
@app.route("/login", methods=["GET","POST"])
def login():
    users = mongo.db.user
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        emaildata = users.find_one({"emailuser":email})
        #passworddata = users.find_one({"mdp":password})
        session['email'] = email
        session['prenom_user'] = emaildata["prenomuser"]
        session['nom_user'] = emaildata["nomuser"]

        if emaildata is None:
            flash("No email", "danger")
            return render_template("login.html")
        
        else:
            # for password_data in passworddata:
                if sha256_crypt.verify(password,emaildata["mdp"]): 
                    flash("LOGIN SUCCESSFULY", "success")
                    return redirect(url_for('index'))
                else:
                    flash("Incorrect password","danger")
                    return render_template("login.html")

    return render_template("login.html")

#logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/chatroom")
def chatrooms():
    return redirect('http://localhost:3000', code=301)

if __name__ == "__main__":
    app.secret_key="klatchEnForce"
    app.run(debug=True)