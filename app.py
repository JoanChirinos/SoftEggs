#SoftEggs
#Britni Canale
#Dennis Chen
#T. Fabiha
#Daniel Gelfand
#pd06


from flask import Flask, render_template, session, request, url_for, redirect, flash
import os
from util import access_data

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route("/")
def hello_world():
    return redirect(url_for("login"))           #Automatically reroutes to login (user must login)


@app.route("/login")
def login():
    if "username" in session:                   #Checks if user is previously signed in
        return render_template("home.html")     #If user logged in previously, goes directly home
    return render_template("login.html")        #If not logged in, prompts user to login


@app.route("/register")
def register():
    return render_template("register.html")     #Displays page allowing user to register

@app.route("/authR", methods = ["POST"])
def authRegister():
    #checks if username is too short
    if request.form['username'].strip(" ") == "" or len(request.form['username'].strip(" ")) < 4:
        #if so, flash an error
        flash("Username is too short")
        return redirect(url_for("register"))  #redirects to register
    #checks if a password exists
    elif request.form['password'].strip(" ") == "":
        flash("No password inputted")
        return redirect(url_for("register"))  #redirects to register
    #checks if passwords are the same in both boxes
    elif request.form['password'] != request.form['confirmpw']:
        #if not, flash an error
        flash("Passwords do not match")
        return redirect(url_for("register"))  #redirects to register
    else:
        access_data.sign_up(request.form['username'].strip(" "), request.form['password'])
        return redirect(url_for("login"))     #redirects to login after successful register

@app.route("/auth", methods=["POST"])
def authorize():
    #if username and pw is correct
    if access_data.login(request.form["username"], request.form["password"]):
    #if request.form['username'] == "dennis" and request.form['password'] == 'abc':
        #put user in session, go to home page
        session['username'] = request.form['username']
        return redirect(url_for("home"))
    else:
        #otherwise flash error and go back to login
        flash("Incorrect Login Information")
        return redirect(url_for("login"))

@app.route('/logout')
def logout():

    #pops user from session, logging out the user
    session.pop('username', None)
    session.pop('password', None)

    #goes back to the login page
    return redirect(url_for('login'))

@app.route("/home") #MUST ADD METHODS, THIS WILL BE USER BASED
def home():
    stories = access_data.view_all(access_data.get_id(session["username"]))
    return render_template("home.html", stories = stories) #Include all info from database afterward to be displayed


@app.route("/view")
def view():
    #Accesses databases to get user-specific information
    return render_template("view.html") #include info from database afterwward to be displayed


@app.route("/add")
def add():
    '''  CHECKS IF USER PREVIOUSLY ADDED, FLASHES ERROR MESSAGE AND REDIRECTS TO VIEW IF SO (we have to pass story to view)
    if access_data.prev_add(n_story, session["username"]):
        flash("You have already added to this story, you cannot add any more entries")
        redirect(url_for("view"))
    '''#Accesses database to get most recent entry
    #return render_template("add.html", storyTitle = "Story Title", prevEntry = access_data.prev_add("storyTitle","id"))
    return render_template("add.html", storyTitle = "Story Title", prevEntry = access_data.view_one("Story Title"))

@app.route("/search", methods=["GET"])
def searchresults():
    #takes info from search textbox
    #checks databases for related stories
    #stories = access_data.stories_of(request.args["input"]))
    return render_template("search.html", results = stories)


@app.route("/create")
def create():
    #Adds new story to database
    return render_template("create.html")

@app.route("/createstory", methods=["GET"])
def createstory():  #adds to database
    #if story already exists
        #return redirect(url_for("create"))
    access_data.create(request.args["storytitle"], request.args["entry"], request.args["tags"], access_data.get_id(session['username']))
    return redirect(url_for("home"))

@app.route("/addStory", methods = ["GET"])
def addStory():
    #add(request.args["storytitle"],request.args["entry"],request.args["tags"], session['username'])
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.debug = True
    app.run()
