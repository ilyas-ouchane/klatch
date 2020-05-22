from flask import Flask , render_template, request, session, logging, url_for, redirect,flash
from flask_pymongo import PyMongo
from passlib.hash import sha256_crypt

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
    return render_template('index.html', nomsChatrooms=nomsChatrooms, preferencesChatrooms=preferencesChatrooms)
#profile
@app.route("/profile")
def profile():
    return render_template('profile.html')

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
        pdp = request.files['pdp']
        pdc = request.files['pdc']

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

        #saving the images on mongodb
        mongo.save_file(pdp.filename, pdp)
        mongo.save_file(pdc.filename, pdc)

        users.insert({"nomuser":nom, "prenomuser":prenom, "emailuser":email, "mdp":secure_password, "pdp_name":pdp.filename, "pdc_name":pdc.filename})
        user = users.find_one({"emailuser":email})
        preferences.insert({"id":user["_id"], "Music":musicG, "Rap":rap, "Raggae":raggae, "Swing":swing, "Jazz":jazz, "Movies":moviesG, "Comedy":comedy, "Romantic":romantic, "Sci-fi":scif, "War":war, "Fantazy/Fairy tales":fantazy, "Documentary":documentary, "Western":western, "History":history, "Psychology":psychology, "Politics":politics, "Reading":reading, "Languages":languages, "Musical instruments":musicalIns, "Writing":writing, "Sport":sport, "Celebrities":celebrities, "Science and technology":science, "Theatre":theatre, "Age":age})

        return redirect(url_for('login'))
    return render_template("register.html")

#creating a chatroom page
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
    preferences = mongo.db.preferences
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        emaildata = users.find_one({"emailuser":email})
        preferences = preferences.find_one({"id":emaildata["_id"]})
        #passworddata = users.find_one({"mdp":password})
        
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
                    session['pdp_name'] = emaildata["pdp_name"]
                    session['pdc_name'] = emaildata["pdc_name"]

                    #include preferences into session
                    session['war'] = preferences["War"]
                    session['music'] = preferences["Music"]
                    session['rap'] = preferences["Rap"]
                    session['raggae'] = preferences["Raggae"]
                    session['swing'] = preferences["Jazz"]
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
        # users = mongo.db.user
        # preferences = mongo.db.preferences

        # #preferences :
        # musicG = request.form.get("musicG")
        # hiphop = request.form.get("hiphop")
        # rap = request.form.get("rap")
        # raggae = request.form.get("raggae")
        # swing = request.form.get("swing")
        # jazz = request.form.get("jazz")
        # moviesG = request.form.get("moviesG")
        # comedy = request.form.get("comedy")
        # romantic = request.form.get("romantic")
        # scif = request.form.get("scif")
        # war = request.form.get("war")
        # fantazy = request.form.get("fantazy")
        # documentary = request.form.get("documentary")
        # western = request.form.get("western")
        # history = request.form.get("history")
        # psychology = request.form.get("psychology")
        # politics = request.form.get("politics")
        # reading = request.form.get("reading")
        # languages = request.form.get("languages")
        # musicalIns = request.form.get("musicalIns")
        # writing = request.form.get("writing")
        # sport = request.form.get("sport")
        # celebrities = request.form.get("celebrities")
        # science = request.form.get("science")
        # theatre = request.form.get("theatre")

        # preferences.update_one({"id":session['idUser']}, {"$set":{"Music":musicG, "Rap":rap, "Raggae":raggae, "Swing":swing, "Jazz":jazz, "Movies":moviesG, "Comedy":comedy, "Romantic":romantic, "Sci-fi":scif, "War":war, "Fantazy/Fairy tales":fantazy, "Documentary":documentary, "Western":western, "History":history, "Psychology":psychology, "Politics":politics, "Reading":reading, "Languages":languages, "Musical instruments":musicalIns, "Writing":writing, "Sport":sport, "Celebrities":celebrities, "Science and technology":science, "Theatre":theatre}})


        return redirect(url_for("profile"))
    return render_template("modifyPref.html")


if __name__ == "__main__":
    app.secret_key="klatchEnForce"
    app.run(debug=True)