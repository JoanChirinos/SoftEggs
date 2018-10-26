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



#=================================AUTHORIZE=====================================

@app.route("/login")
def login():
    '''Function for /login, checks if user is already logged in

    If user is logged in, redirects to /home
    If user is not logged in, opens login.html
    '''
    if "username" in session:
        return redirect(url_for("home"))
    return render_template("login.html")



@app.route("/register")
def register():
    '''Displays page allowing users without accounts to register'''
    return render_template("register.html")



@app.route("/authR", methods = ["POST"])
def authRegister():
    '''Checks if inputs for new user are allowed

    Checks if username is long enough, flashes message and goes back to register if not
    Checks if password is input, flashes message and goes back to register if not
    Checks if passwords match, flashes message and goes back to register if not

    If all tests passed, user information is added to database and user is redirected to login
    '''

    if request.form['username'].strip(" ") == "" or len(request.form['username'].strip(" ")) < 4:
        flash("Username is too short")
        return redirect(url_for("register"))
    elif request.form['password'].strip(" ") == "":
        flash("No password input")
        return redirect(url_for("register"))
    elif request.form['password'] != request.form['confirmpw']:
        flash("Passwords do not match")
        return redirect(url_for("register"))
    else:
        if not access_data.sign_up(request.form['username'].strip(" "), request.form['password']):
            flash("Username taken")
            return redirect(url_for("register"))
        return redirect(url_for("login"))



@app.route("/auth", methods=["POST"])
def authorize():
    '''Checks is user information input for login is Incorrect

    Checks if the username-password pair exists in the database
    If not,flashes message and redirects to login.
    If so, redirects to home
    '''
    #try:
    #    if session['username']:
    #        redirect(url_for('logout'))
    #except:
    #    pass
    if access_data.login(request.form["username"], request.form["password"]):
        session['username'] = request.form['username']
        return redirect(url_for("home"))
    else:
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





#===================================VIEW========================================

@app.route("/home")
def home():
    '''Displays home page for specific user

    Accesses database to retrieve stories that the user has already edited,
    displays those stories in full on home page.
    '''
    if "username" not in session:
        return redirect(url_for("login"))
    def ridOfUScore(uScoreTitle):
        return " ".join(uScoreTitle.split("_"))
    stories = access_data.view_all(access_data.get_id(session["username"]))
    storyInfo = dict()
    storytags = dict()
    for story in stories:
        storytags[story] = access_data.all_tags(story)
        title = "_".join(story.split(" "))
        content = "_".join(stories[story])
        storyInfo[title] = content
        print(storytags[story])
    return render_template("home.html",storyStuff = storyInfo, storytags= storytags, spaceJoin = ridOfUScore)



@app.route("/view")
def view():
    '''    Allows user to view individual story (previously edited) on a single page    '''
    if "username" not in session:
        return redirect(url_for("login"))
    title = " ".join(request.args['title'].split("_"))
    sContent = request.args['content'].split("_")
    return render_template("view.html",story = title, content = sContent) #include info from database afterward to be displayed



@app.route("/allstories")
def viewAllS():
    ''' Displays all stories in databases'''
    if "username" not in session:
        return redirect(url_for("login"))
    storyLinks = dict()
    stories = access_data.all_stories()
    for story in stories:
        storyLinks[story] = ("/add?title=" + "_".join(story.split(" ")) + "&" + "content=" + "_".join(access_data.view_one(story).split(" ")))
    storytags = dict()
    for story in stories:
        print(story)
        storytags[story] = access_data.all_tags(story)
        print(storytags[story])
    return render_template("allstories.html", links = storyLinks, storytags = storytags)

#=================================ADD ENTRY=====================================

@app.route("/add")
def add():
    '''Displays page allowing user to add to specific storyLink

    Checks if user previously added, redirects to view and flashes error if so
    If not, displays page with most recent entry of story and textbox for the user's new entry
    '''
    if "username" not in session:
        return redirect(url_for("login"))
    sTitle = " ".join(request.args["title"].split("_"))
    if access_data.prev_add(sTitle, access_data.get_id(session["username"])):
        flash("You have already added to that story, you cannot add any more entries")
        return redirect(url_for("home"))
    previousEntry = " ".join(request.args['content'].split("_"))
    title = request.args['title']
    return render_template("add.html", storyTitle = sTitle, prevEntry = previousEntry, storTitle = title)



@app.route("/addStory", methods = ["GET","POST"])
def addStory():
    ''' Adds entry to the story

    If the entry is empty, flashes an error
    Title of story and content of your entry is passed into the database, then you're redirected to home
    '''
    if "username" not in session:
        return redirect(url_for("login"))
    if request.form["entry"].strip(" ") == "":
        flash("Please Create an Entry")
        return redirect(url_for("add"))
    sTitle = " ".join(request.args['title'].split("_"))
    sContent = request.form['entry']
    access_data.add(sTitle,sContent,access_data.get_id(session['username']))
    return redirect(url_for("home"))


@app.route("/search", methods=["GET"])
def searchresults():
    '''Displays search search results

    Compares input with tags and titles in databases and displays links to those that match
    '''
    if "username" not in session:
        return redirect(url_for("login"))
    def ridOfUScore(uScoreTitle):
        return " ".join(uScoreTitle.split("_"))
    storyStuff = dict()
    stories = access_data.stories_of(request.args['input'])
    for story in stories:
        title = "_".join(story.split(" "))
        content = "_".join(access_data.view_one(story).split(" "))
        storyStuff[title] = content
    #if access_data.exists(request.args['input'])["title"]:
    #    storyStuff[request.form["input"]] = content
    return render_template("search.html", storyStuff = storyStuff, spaceJoin = ridOfUScore)



#================================CREATE STORY===================================

@app.route("/create")
def create():
    '''Opens page allowing user to create new story'''
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("create.html")



@app.route("/createstory", methods=["GET"])
def createstory():
    '''Adds input story to databases

    Checks if everything has an input value:
    If not, flashes error and redirects to /create
    If so, checks if input story has same title as existing story:
    If it matches existing story, flashes error and redirects to /create
    If it meets requirements, story is added to database and user is redirected to /home
    '''
    if "username" not in session:
        return redirect(url_for("login"))
    if (request.args["storytitle"].strip(" ") == "" or
        request.args["entry"].strip(" ") == "" or
        request.args["tags"].strip(" ") == ""):
        flash("Please Fill Out Everything")
        return redirect(url_for("create"))
    if access_data.create(request.args["storytitle"], request.args["entry"], request.args["tags"], access_data.get_id(session['username'])):
        return redirect(url_for("home"))
    else:
        flash("A story with this title is taken")
        return redirect(url_for("create"))



#====================================RUN========================================

if __name__ == "__main__":
    app.debug = True
    app.run()
