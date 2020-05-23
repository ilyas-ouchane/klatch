from flask import Flask , render_template, request, session, logging, url_for, redirect,flash
from flask_pymongo import PyMongo
from passlib.hash import sha256_crypt
from sklearn import svm
from sklearn import metrics
import pickle
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

import sklearn
from sklearn import datasets
from sklearn import metrics

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

# pd.set_option('display.width', 5000
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
import sklearn
import pandas as pd
import numpy as np
from sklearn import linear_model

from sklearn import metrics
import pickle

import pickle
import random
import time

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'klatch'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/klatch'

mongo = PyMongo(app)

data = pd.read_csv('5clustKlatch.csv', sep=';')
data = data[['Music', 'Hiphop, Rap', 'Raggae', 'Swing, Jazz', 'Movies',
       'Comedy', 'Romantic', 'Sci-fi', 'War', 'Fantasy/Fairy tales',
       'Documentary', 'Western', 'History', 'Psychology', 'Politics',
       'Reading', 'Languages', 'Musical instruments', 'Writing', 'Sport',
       'Celebrities', 'Science and technology', 'Theatre', 'Age', 'Gender',
       'clusters']]
predict = 'clusters'

X = np.array(data.drop([predict], 1))
Y = np.array(data[predict])

X=X.astype('int')
Y=Y.astype('int')


x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, Y, test_size=0.1)


clf = svm.SVC(kernel="linear") #On peut donner en paramètre kernel and soft margin of the hyperplan
clf.fit(x_train, y_train)


# clf.fit(x_train, y_train)

y_pred = clf.predict(x_test) # Predict values for our test data

acc = metrics.accuracy_score(y_test, y_pred) # Test them against our correct values

scores = cross_val_score(clf, X, Y, cv=30)
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
    preferencesChatrooms = crPreferences.find({}, {"Music":1,  "Raggae":1, "Swing":1, "Movies":1, "Comedy":1, "Romantic":1, "Sci-fi":1, "War":1, "Fantazy/Fairy tales":1, "Documentary":1, "Western":1, "History":1, "Psychology":1, "Politics":1, "Reading":1, "Languages":1, "Musical instruments":1, "Writing":1, "Sport":1, "Celebrities":1, "Science and technology":1, "Theatre":1})
    preferencesTab = ["Music", "Raggae", "Swing", "Movies", "Comedy", "Romantic", "Sci-fi", "War", "Fantazy/Fairy tales", "Documentary", "Western", "History", "Psychology", "Politics", "Reading", "Languages", "Musical instruments", "Writing", "Sport", "Celebrities", "Science and technology", "Theatre"]
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
    preferencesChatrooms = crPreferences.find({}, {"Music":1, "Raggae":1, "Swing":1, "Movies":1, "Comedy":1, "Romantic":1, "Sci-fi":1, "War":1, "Fantazy/Fairy tales":1, "Documentary":1, "Western":1, "History":1, "Psychology":1, "Politics":1, "Reading":1, "Languages":1, "Musical instruments":1, "Writing":1, "Sport":1, "Celebrities":1, "Science and technology":1, "Theatre":1})
    preferencesTab = ["Music", "Raggae", "Swing", "Movies", "Comedy", "Romantic", "Sci-fi", "War", "Fantazy/Fairy tales", "Documentary", "Western", "History", "Psychology", "Politics", "Reading", "Languages", "Musical instruments", "Writing", "Sport", "Celebrities", "Science and technology", "Theatre"]
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
    def test_model(list):
            pickle.dump(clf, open('final_model_klatch.sav', 'wb'))
            loaded_model = pickle.load(open('final_model_klatch.sav', 'rb'))
            A = np.array(list)
            B = A.reshape(1,-1)
            result = loaded_model.predict(B)
            return result[0]
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
        pdp = request.files['pdp']
        pdc = request.files['pdc']

        #preferences :
        musicG = request.form.get("musicG")
        hiphop = request.form.get("hiphop")
        raggae = request.form.get("raggae")
        swing = request.form.get("swing")
        moviesG = request.form.get("moviesG")
        comedy = request.form.get("comedy")
        romantic = request.form.get("romantic")
        scif = request.form.get("scif")
        war = request.form.get("war")
        fantazy = request.form.get("fantasy")
        documentary = request.form.get("documentaries")
        western = request.form.get("western")
        history = request.form.get("history")
        psychology = request.form.get("psychology")
        politics = request.form.get("politics")
        reading = request.form.get("reading")
        languages = request.form.get("languages")
        musicalIns = request.form.get("instruments")
        writing = request.form.get("writing")
        sport = request.form.get("sports")
        celebrities = request.form.get("celebrities")
        science = request.form.get("technology")
        theatre = request.form.get("theater")

        ######################## Testing the model##########################################
        list=[musicG,hiphop,raggae,swing,moviesG,comedy,romantic,scif,war,fantazy,documentary,western,history,psychology,
        politics,reading,languages,musicalIns,writing,sport,celebrities,science,theatre,age,genre]

        #saving the images on mongodb
        mongo.save_file(pdp.filename, pdp)
        mongo.save_file(pdc.filename, pdc)

        cr = test_model(list)
        users.insert({"nomuser":nom, "prenomuser":prenom, "emailuser":email, "mdp":secure_password, "cr": int(cr), "pdp_name":pdp.filename, "pdc_name":pdc.filename})
        user = users.find_one({"emailuser":email})
        preferences.insert({"id":user["_id"], "Music":musicG, "HipHop":hiphop, "Raggae":raggae, "Swing":swing, "Movies":moviesG, "Comedy":comedy, "Romantic":romantic, "Sci-fi":scif, "War":war, "Fantazy/Fairy tales":fantazy, "Documentary":documentary, 
        "Western":western, "History":history, "Psychology":psychology, "Politics":politics, "Reading":reading, "Languages":languages, "Musical instruments":musicalIns, "Writing":writing, "Sport":sport, "Celebrities":celebrities, "Science and technology":science, 
        "Theatre":theatre, "Age":age, "Genre": genre})

        return redirect(url_for('login'))
    return render_template("register.html")

#register page
@app.route("/create_chatroom", methods=["GET", "POST"])
def create_chatroom():
    if request.method == "POST":
        chatrooms = mongo.db.chatroom
        chatroompreferences = mongo.db.chatroompreferences
        #chatroom_info
        nomcr = request.form.get("nomcr")
        descr = request.form.get("descr") 
        pdpch = request.files['pdpch']  
        #preferences :
        musicG = request.form.get("musicG")
        hiphop = request.form.get("hiphop")
        raggae = request.form.get("raggae")
        swing = request.form.get("swing")
        moviesG = request.form.get("moviesG")
        comedy = request.form.get("comedy")
        romantic = request.form.get("romantic")
        scif = request.form.get("scif")
        war = request.form.get("war")
        fantazy = request.form.get("fantasy")
        documentary = request.form.get("documentaries")
        western = request.form.get("western")
        history = request.form.get("history")
        psychology = request.form.get("psychology")
        politics = request.form.get("politics")
        reading = request.form.get("reading")
        languages = request.form.get("languages")
        musicalIns = request.form.get("instruments")
        writing = request.form.get("writing")
        sport = request.form.get("sports")
        celebrities = request.form.get("celebrities")
        science = request.form.get("technology")
        theatre = request.form.get("theater")

        #saving the images on mongodb
        mongo.save_file(pdpch.filename, pdpch)

        chatrooms.insert({"nomchatroom":nomcr, "description":descr, "pdpch":pdpch.filename})
        session['chatroom'] = nomcr
        chatroom = chatrooms.find_one({"nomchatroom":nomcr})
        chatroompreferences.insert({"id":chatroom["_id"], "Music":musicG,"Raggae":raggae, "Swing":swing, "Movies":moviesG, "Comedy":comedy, "Romantic":romantic, "Sci-fi":scif, "War":war, "Fantazy/Fairy tales":fantazy, "Documentary":documentary, "Western":western, "History":history, "Psychology":psychology, "Politics":politics, "Reading":reading, "Languages":languages, "Musical instruments":musicalIns, "Writing":writing, "Sport":sport, "Celebrities":celebrities, "Science and technology":science, "Theatre":theatre})

        session['pdpch'] = chatroom["pdpch"] 

        return redirect(url_for('index'))
    return render_template("create_chatroom.html")    

#login
@app.route("/login", methods=["GET","POST"])
def login():
    users = mongo.db.user
    preferences = mongo.db.preferences
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        emaildata = users.find_one({"emailuser":email})
        preferences = preferences.find_one({"id":emaildata["_id"]})

        if emaildata is None:
            flash("No email", "danger")
            return render_template("login.html")
        
        else:
            # for password_data in passworddata:
                if sha256_crypt.verify(password,emaildata["mdp"]): 
                    flash("LOGIN SUCCESSFULY", "success")
                    session['email'] = email
                    session['prenom_user'] = emaildata["prenomuser"]
                    session['nom_user'] = emaildata["nomuser"]
                    session['cr'] = emaildata["cr"]
                    session['pdp_name'] = emaildata["pdp_name"]
                    session['pdc_name'] = emaildata["pdc_name"]

                    #include preferences into session
                    session['war'] = preferences["War"]
                    session['music'] = preferences["Music"]
                    session['raggae'] = preferences["Raggae"]
                    session['movies'] = preferences["Movies"]
                    session['comedy'] = preferences["Comedy"]
                    session['romantic'] = preferences["Romantic"]
                    session['scif'] = preferences["Sci-fi"]
                    session['fantazy'] = preferences["Fantazy/Fairy tales"]
                    session['documentary'] = preferences["Documentary"]
                    session['western'] = preferences["Western"]
                    session['history'] = preferences["History"]
                    session['psy'] = preferences["Psychology"]
                    session['politics'] = preferences["Politics"]
                    session['reading'] = preferences["Reading"]
                    session['lang'] = preferences["Languages"]
                    session['musicalins'] = preferences["Musical instruments"]
                    session['writing'] = preferences["Writing"]
                    session['sport'] = preferences["Sport"]
                    session['celeb'] = preferences["Celebrities"]
                    session['sci'] = preferences["Science and technology"]
                    session['theatre'] = preferences["Theatre"]

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

#to send the images from the DB
@app.route("/file/<filename>")
def file(filename):
    return mongo.send_file(filename)

@app.route("/modifyPref", methods=["GET","POST"])
def modifyPref():
    if request.method == "POST":
        return redirect(url_for("profile"))
    return render_template("modifyPref.html")

if __name__ == "__main__":
    app.secret_key="klatchEnForce"
    app.run(debug=True)