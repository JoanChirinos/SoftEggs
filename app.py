#SoftEggs
#Britni Canale
#Dennis Chen
#T. Fabiha
#Daniel Gelfand
#pd06


from flask import Flask, render_template, session, request, url_for, redirect, flash

app = Flask(__name__)

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


@app.route("/auth", methods=["POST"])
def authorize():
    #if log_in(request.form["username"], request.form["password"]):
    if request.form['username'] == "dennis" and request.form['password'] == 'abc':
        session['username'] = request.args['username']
        return redirect(url_for("home"))
    else:
        flash("Incorrect Login Information")
        return redirect(url_for("login"))


@app.route("/home") #MUST ADD METHODS, THIS WILL BE USER BASED
def home():
    #Takes info from form
    #Adds to session
    #Accesses databases to get user-specific information
    return render_template("home.html") #Include all info from database afterward to be displayed


@app.route("/view")
def view():
    #Accesses databases to get user-specific information
    return render_template("view.html") #include info from database afterwward to be displayed


@app.route("/add")
def add():
    #Accesses database to get most recent entry
    return render_template("add.html")


@app.route("/search")
def searchresults():
    #takes info from search textbox
    #checks databases for related stories
    return render_template("search.html")


@app.route("/create")
def create():
    #Adds new story to database
    return render_template("create.html")



if __name__ == "__main__":
    app.debug = True
    app.run()
