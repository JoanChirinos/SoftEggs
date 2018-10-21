import sqlite3


DB_FILE="discoeggs.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()

def login(user,pwd):
    return true

def view_one(story):

    command = "SELECT content from stories WHERE story_name = \'"+  story + "\'"
    c.execute(command)
    contents = c.fetchall()
    #Get last element in array and then last elemtnt in the list that lies inside the array
    #print(contents[-1][-1])
    return (contents[-1][-1])

#view_one("egg boss")

def view_all(id):
    #stores where the editor has added to the stories
    command = "SELECT content from stories WHERE editor_id = \'"+  id + "\'"
    c.execute(command)
    contents = c.fetchall()
    return(contents[-1])
