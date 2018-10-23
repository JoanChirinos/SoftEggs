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
    '''Function for root route, immediately reroutes to /login'''
    return redirect(url_for("login"))



@app.route("/login")
def login():
    '''Function for /login, checks if user is already logged in

    If user is logged in, redirects to /home
    If user is not logged in, opens login.html
    '''
    if "username" in session:                   #Checks if user is previously signed in
        return redirect(url_for("home"))        #If user logged in previously, goes directly home
    return render_template("login.html")        #If not logged in, prompts user to login



@app.route("/register")
def register():
    '''Displays page allowing users without accounts to register'''
    return render_template("register.html")     #Displays page allowing user to register



@app.route("/authR", methods = ["POST"])
def authRegister():
    '''Checks if inputs for new user are allowed

    Checks if username is long enough, flashes message and goes back to register if not
    Checks if password is input, flashes message and goes back to register if not
    Checks if passwords match, flashes message and goes back to register if not

    If all tests passed, user information is added to database and user is redirected to login
    '''
    #checks if username is too short
    if request.form['username'].strip(" ") == "" or len(request.form['username'].strip(" ")) < 4:
        #if so, flash an error
        flash("Username is too short")
        return redirect(url_for("register"))  #redirects to register
    #checks if a password exists
    elif request.form['password'].strip(" ") == "":
        flash("No password input")
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
    '''Checks is user information input for login is Incorrect

    Checks if the username-password pair exists in the database
    If not,flashes message and redirects to login.
    If so, redirects to home
    '''
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
    '''Logouts user from session

    Pops (removes) username and password from session
    Redirects to login page
    '''
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('login'))



@app.route("/home")
def home():
    '''Displays home page for specific user

    Accesses database to retrieve stories that the user has already edited,
    displays those stories in full on home page.
    '''
    stories = access_data.view_all(access_data.get_id(session["username"]))
    return render_template("home.html",stories = stories) #Include all info from database afterward to be displayed



@app.route("/view")
def view():
    '''NOT CURRENTLY IN USE

    Allows user to view individual story (previously edited) on a single page
    '''
    return render_template("view.html") #include info from database afterwward to be displayed



@app.route("/add")
def add():
    '''Displays page allowing user to add to specific storyLink

    Checks if user previously added, redirects to view and flashes error if so
    If not, displays page with most recent entry of story and textbox for the user's new entry
    '''
    #if access_data.prev_add(n_story, session["username"]):
        #flash("You have already added to this story, you cannot add any more entries")
        #redirect(url_for("view"))
    #Accesses database to get most recent entry
    #return render_template("add.html", storyTitle = "Story Title", prevEntry = access_data.prev_add("storyTitle","id"))
#sTitle = request.args["story"]
    #previousEntry = request.args['storyContent']
    return render_template("add.html", storyTitle = sTitle, prevEntry = previousEntry)



@app.route("/search", methods=["GET"])
def searchresults():
    '''Displays search search results

    Compares input with tags and titles in databases and displays links to those that match
    '''
    #takes info from search textbox
    #checks databases for related stories
    #storyLinks = []
    #for story in stories:
    #    storyLinks.append("/add?title=" + story + "&" + "content=" + view_one(story))
    #return render_template("search.html", results = stories, links = storyLinks)
    return render_template("search.html", results = stories)



@app.route("/create")
def create():
    '''Opens page allowing user to create new story'''
    #Adds new story to database
    return render_template("create.html")



@app.route("/createstory", methods=["GET"])
def createstory():
    '''Adds input story to databases


    '''
     #adds to database
    #if story already exists
        #return redirect(url_for("create"))
    if (request.args["storytitle"].strip(" ") == "" or
        request.args["entry"].strip(" ") == "" or
        request.args["tags"].strip(" ") == ""):
        flash("Please Fill Out Everything")
        return redirect(url_for("create"))
    access_data.create(request.args["storytitle"], request.args["entry"], request.args["tags"], access_data.get_id(session['username']))
    return redirect(url_for("home"))



@app.route("/addStory", methods = ["GET"])
def addStory():
    #add(request.args["storytitle"],request.args["entry"],request.args["tags"], session['username'])
    if request.args["entry"].strip(" ") == "":
        flash("Please Create an Entry")
        return redirect(url_for("add"))
    return redirect(url_for("home"))



if __name__ == "__main__":
    app.debug = True
    app.run()
