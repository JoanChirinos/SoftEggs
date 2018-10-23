import sqlite3

def sign_up(user, pwd):
    DB_FILE="data/discoeggs.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()

    command = "SELECT COUNT(*) FROM login WHERE username = \"{}\"".format(user)
    c.execute(command)
    rows = c.fetchone()
    if(rows != None):
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

#print(sign_up("Scriptor","nah"))
#print(sign_up("Scriptor","nah"))

def login(user,pwd):
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
    if password == None or password[0] != pwd:
        return False

    return True

'''
login('bob', 'bobby')
print(login('bobby','bobbster')) #False
print(login('bobby','bobster')) #True
'''
def view_one(story):
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
    return (contents[-1][-1])

#view_one("egg boss")


def view_all(id):
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

        #[('Once upon a time there was an egg boss.',), ('His name was Humpty Dumpty',)]

        #Getting the insides of the wholeContent
        ret[story[0]] = content #creates a new key for a story with all its content

    db.commit() #save changes
    db.close()  #close database

    return ret


#view_all(1)


def get_id(user):
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


    splitted = tags.split(",")
    for i in range(len(splitted)):
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
    '''Gives the stories associated with the provided tag'''

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
    if(prev_add(n_story,id)):
        return False

    DB_FILE= "data/discoeggs.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()

    command = "SELECT COUNT(story_name) FROM stories WHERE story_name=\"{}\"".format(n_story)
    c.execute(command)
    numTuple = c.fetchone()
    if (len(numTuple) == None):
        return False
    num = numTuple[0]
    #print(splitted)
    # check to make sure story name doesnt exist yet
    params = (n_story,content, num+1, id)
    command = "INSERT INTO stories VALUES(?,?,?,?)"
    c.execute(command,params)

    db.commit()
    db.close()
    return True
#print(add("egg boss", "He was so cool.", 19))
