#SoftEggs
#Britni Canale
#Dennis Chen
#T. Fabiha
#Daniel Gelfand
#pd06


import sqlite3

'''The code below is used to access data from the database based on the user's needs'''

def createDatabase():
    ''' Creates a database if user decided to delete the database '''


    DB_FILE="data/discoeggs.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()

    command = "CREATE TABLE IF NOT EXISTS login(username TEXT, password TEXT, editor_id INTEGER PRIMARY KEY)"
    c.execute(command)

    command = "CREATE TABLE IF NOT EXISTS stories(story_name TEXT, content TEXT, entry_num INTEGER, editor_id INTEGER)"
    c.execute(command)

    command = "CREATE TABLE IF NOT EXISTS tags(story_name TEXT, tag TEXT)"
    c.execute(command)

    db.commit()
    db.close()


def sign_up(user, pwd):
    '''sign_up adds a usernam and its associated password if the user does not exist yet'''

    createDatabase()

    DB_FILE="data/discoeggs.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()

    command = "SELECT COUNT(*) FROM login WHERE username = \"{}\"".format(user)
    c.execute(command)
    rows = c.fetchone()
    if(rows[0] != 0):
        #print(rows[0])
        return False;

    #still have to make sure that we cannot create multiple of the same users

    #we gotta find out how many rows there are already
    #see what happens now using that
    command = "SELECT COUNT(*) FROM login"

    c.execute(command)
    rows = c.fetchone()[0]
    #print(rows)
    params = (user, pwd, rows+1)
    c.execute("INSERT INTO login VALUES (?,?,?)", params)

    db.commit() #save changes
    db.close()  #close database

    return True

#print(sign_up("Potatoma","potato"))
#print(sign_up("Scripto","nah"))

def login(user,pwd):
    '''login returns True if the username and password provided match. Otherwise, returns False.'''

    createDatabase()

    DB_FILE="data/discoeggs.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()

    command = "SELECT password FROM login WHERE username = \'{}\'".format(user)
    c.execute(command)
    password = c.fetchone()
    #print(password)

    db.commit() #save changes
    db.close()  #close database

    #print(password);

    #If no password for that user or the password does not match the inputted password
    if password == None or password[0] != pwd:
        return False

    return True

'''
#login('bob', 'bobby')
print(login('Potatoman','potato')) #False
print(login('bobby','bobster')) #True
'''
def view_one(story):
    '''Given a story, this method accesses and returns the latest paragraph from that story'''

    createDatabase()

    DB_FILE="data/discoeggs.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()

    command = "SELECT content FROM stories WHERE story_name = \'{}\'".format(story)
    c.execute(command)
    contents = c.fetchall()

    db.commit() #save changes
    db.close()  #close database

    #Get last element in array and then last elemtnt in the list that lies inside the array
    #print(contents[-1][-1])

    #Get latest content for given story
    return (contents[-1][-1])

#view_one("egg boss")


def view_all(id):
    '''Accesses the contents of the stories the user has added to.'''

    createDatabase()

    DB_FILE="data/discoeggs.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()

    #stores where the editor has added to the stories
    command = "SELECT story_name FROM stories WHERE editor_id = {}".format(id)
    c.execute(command)
    stories = c.fetchall()
    #print(contents)
    ret = {}

    for story in stories:

        #Gets the story name from the tuple
            #print(each[0])
            #Using each[0] bc each is a tuple
        #Selects the content of the story with the same story name that each[0] holds

        command = "SELECT content FROM stories WHERE story_name = \'{}\'".format(story[0])
        c.execute(command)
        #Refers to content with tuple and list outside
        uneditedContent = c.fetchall()

        content = []

        for each in uneditedContent:
            content.append(each[0])


        ret[story[0]] = content #creates a new key for a story with all its content

    db.commit() #save changes
    db.close()  #close database

    return ret


#view_all(1)


def get_id(user):
    '''Returns the associated editor_id with a username'''

    createDatabase()

    DB_FILE="data/discoeggs.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()

    command = "SELECT editor_id FROM login WHERE username = \'{}\' ".format(user)
    #print(command)
    c.execute(command)
    id = c.fetchone()
    #print(id[-1])

    db.commit() #save changes
    db.close()  #close database

    return(id[-1])

def create(n_story, content, tags, id):
    '''Creates a new story in the database with given content.
    Tags are provided to be later used for searching for stories'''

    createDatabase()

    DB_FILE= "data/discoeggs.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()

    #print(splitted)
    # check to make sure story name doesnt exist yet
    command = "SELECT story_name FROM stories WHERE story_name = \'{}\'".format(n_story)
    c.execute(command)

    #Retrieve the story with provided story name
    story = c.fetchall()
    #print(storyNames)
    #print(story)
    if (len(story) != 0):
        # return False # if story name exists
        return False

    # add in story, content, 1, editor_id
    params = (n_story, content, 1, id)
    command = "INSERT INTO stories VALUES(?,?,?,?)"
    c.execute(command,params)

    #Split tags based on commas
    splitted = tags.split(",")
    for i in range(len(splitted)):
        #Getting rid of the spaces
        splitted[i] = splitted[i].replace(" ", "")

        params = (n_story, splitted[i])
        command = "INSERT INTO tags VALUES(?,?)"
        c.execute(command,params)

    db.commit() #save changes
    db.close()  #close database

    return True

#create("Fights", "There were fights.", "fights,fight hood", 1 )

#Checks if user has previously added to a given story
#Returns true if the user have added previously, false otherwise
def prev_add(n_story,id):
    '''Checks if an editor has previously added to a story.
       Return True if the editor has added before, False otherwise'''

    createDatabase()

    DB_FILE= "data/discoeggs.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()

    command = "SELECT editor_id FROM stories WHERE story_name = \"{}\" ".format(n_story)
    c.execute(command)

    ids = c.fetchall()
    db.commit()
    db.close()
    #print(ids)
    for each in ids:
        if (each[0]==id):
            #Returns True if editor prevously added to the given story
            return True
    #Editor has not added previously to givn story
    return False

#prev_add("egg boss", 1)

def stories_of(tag):
    '''Returns the stories associated with the provided tag'''

    createDatabase()

    DB_FILE= "data/discoeggs.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()

    noSpaces = tag.replace(' ', '')
    command = "SELECT story_name from tags where tag=\"{}\" ".format(noSpaces)
    c.execute(command)

    stories = c.fetchall()
    db.commit()
    db.close()

    if (len(stories) == 0):
        return ""
    ret = []
    for each in stories:
        ret.append(each[0])

    return ret
#stories_of("egg")

def add(n_story,content,id):
    '''Adds a new paragraph to a story in the database
        id is used to view which user made the edit
    '''

    createDatabase()

    #Check if editor has added to this story before
    if(prev_add(n_story,id)):
        #don't let editor add again
        return False

    DB_FILE= "data/discoeggs.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()

    command = "SELECT COUNT(story_name) FROM stories WHERE story_name=\"{}\"".format(n_story)
    c.execute(command)
    numTuple = c.fetchone()

    #Check if such story exists
    if (len(numTuple) == None):
        return False
    #Extract the number from the tuple
    num = numTuple[0]
    #print(splitted)

    params = (n_story,content, num+1, id)
    command = "INSERT INTO stories VALUES(?,?,?,?)"
    c.execute(command,params)

    db.commit()
    db.close()
    return True
#print(add("egg boss", "He was so cool.", 19))

def all_stories():
    createDatabase()

    DB_FILE= "data/discoeggs.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()

    command = "SELECT story_name from stories"
    c.execute(command)

    stories = c.fetchall()
    db.commit()
    db.close()

    if (len(stories) == 0):
        return ""

    ret = []
    for each in stories:
        ret.append(each[0])

    return ret

#print(all_stories())

def all_tags(single):
    createDatabase()

    DB_FILE= "data/discoeggs.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()

    command = "SELECT tag FROM tags WHERE story_name=\'{}\'".format(single)
    c.execute(command)

    stags = c.fetchall()
    db.commit()
    db.close()

    if (len(stags) == 0):
        return ""

    ret = []
    for each in stags:
        ret.append(each[0])

    return ret

#print(all_tags("egg boss"))
#print(all_tags("pie"))
