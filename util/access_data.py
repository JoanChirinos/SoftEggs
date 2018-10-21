import sqlite3

DB_FILE="./data/discoeggs.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()

def sign_up(user, pwd):
    #we gotta find out how many rows there are already
    #see what happens now using that
    command = "SELECT COUNT(*) FROM login"
    c.execute(command)
    rows = c.fetchone()[0]
    #print(rows)
    params = (user, pwd, rows+1)
    c.execute("INSERT INTO login VALUES (?,?,?)", params)
    return True

sign_up("Scriptor","nah")

def log_in(user,pwd):
    command = "SELECT password FROM login WHERE username = \'{}\'".format(user)
    c.execute(command)
    password = c.fetchone()[0]
    #print(password)
    if pwd == password:
        return True

    return False
'''
print(login('bobby','bobbster')) #False
print(login('bobby','bobster')) #True
'''
def view_one(story):

    command = "SELECT content FROM stories WHERE story_name = \'{}\'".format(story)
    c.execute(command)
    contents = c.fetchall()
    #Get last element in array and then last elemtnt in the list that lies inside the array
    #print(contents[-1][-1])
    return (contents[-1][-1])

#view_one("egg boss")


def view_all(id):
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

    return ret


view_all(1)


def get_id(user):
    command = "SELECT editor_id FROM login WHERE username = \'{}\' ".format(user)
    #print(command)
    c.execute(command)
    id = c.fetchone()
    #print(id[-1])
    return(id[-1])

db.commit() #save changes
db.close()  #close database
