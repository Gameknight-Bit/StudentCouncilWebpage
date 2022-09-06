#This script creates and manipulates .json files for the html of each event page#

###################
## Documentation ##
###################
# Steps (to create new event):
# 1. run cmd 'python -c "import events; events.init()"'
# 2. enter in "1"
# 3. enter in information
#   - Image Link/src (can be "none" or "na" or "")
#   - Title of article
#   - Small description of article
####################

import json
import datetime
from os.path import exists
#from operator import truediv
import uuid

## EventCard ##
class EventCard:
    def __init__(self, title, shortdesc, date = datetime.datetime.now().strftime("%m/%d/%Y"), img="https://ksr-ugc.imgix.net/assets/011/564/243/fe08249a3130825629831c018799d110_original.jpg?ixlib=rb-4.0.2&crop=faces&w=1024&h=576&fit=crop&v=1463684536&auto=format&frame=1&q=92&s=5a2e2ca44b36406651c01c8b849c61b6"):
        self.img = img
        self.title = title
        self.desc = shortdesc
        self.date = date
        self.UUID = str(uuid.uuid4().hex) #unique identifier for eventcard

    def todict(self):
        return {"img": self.img ,"title": self.title, "desc": self.desc, "date": self.date, "UUID": self.UUID}

    def fromdict(self, dict):
        self.img = dict["img"]
        self.title = dict["title"]
        self.desc = dict["desc"]
        self.date = dict["date"]
        self.UUID = dict["UUID"] #unique identifier for eventcard

    def genUUID(self):
        id = str(uuid.uuid4().hex)
        self.UUID = id
        return id
################

#returns true if event exists (false else)
def eventExists(id):
    with open("database/events.json", "r+") as f:
        data = json.load(f)
        if str(id) in data:
            return True
        else:
            return False

#Returns None#
def newEvent(title, shortdesc, img="", html="<p>No Event Info Avaliable...</p>", date = datetime.datetime.now().strftime("%m/%d/%Y")):
    with open("database/events.json", "r+") as f:
        data = json.load(f)
        if img == "":
            newCard = EventCard(title, shortdesc, date)
        else:
            newCard = EventCard(title, shortdesc, date, img)
        
        id = newCard.genUUID()
        data[id] = {
            "eventCard": newCard.todict(),
            "source": html,
            "date": date,
            "author": "Student Council",
            "UUID": id,
        }
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

#Returns None#
def insertHtml(data, html): #data should be dictionary of event
    with open("database/events.json", "r+") as f:
        d = json.load(f)
        d[str(data["UUID"])]["source"] = " ".join(str.splitlines(html)).replace('"', "'")
        f.seek(0)
        json.dump(d, f, indent=4)
        f.truncate()

#Returns True if successful#
def deleteEvent(id):
    if eventExists(id):
        with open("database/events.json", "r+") as f:
            data = json.load(f)
            data.pop(id)
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        return True
    else:
        return False

#Returns list of event dictonaries (default len = 0)
def getEvents(len=0, sortMethod="date"):
    with open("database/events.json", "r+") as f:
        rawdata = json.load(f)
        if str.lower(sortMethod)=="olddate":
            data = sorted(rawdata.values(), key=lambda d: datetime.datetime.strptime(d["date"], "%m/%d/%Y"))
        else:
            data = sorted(rawdata.values(), key=lambda d: datetime.datetime.strptime(d["date"], "%m/%d/%Y"), reverse=True)
        if len == 0:
            return data
        else:
            return data[0:len]

#Returns event dictorary or None#
def getEventFromID(id):
    if eventExists(id):
        with open("database/events.json", "r+") as f:
            data = json.load(f)
            return data[id]
    else:
        return None

def getEventFromTitle(title):
    with open("database/events.json", "r+") as f:
        data = json.load(f)
        for v in data.values():
            if v["eventCard"]["title"] == title:
                return v
        return None

##############################
## User Friendly Section :) ##
##############################
def init():
    print("------- Event Editor -----")
    print("Version 1.0.0")
    print("Connecting to events.json file...")
    if not exists("database/events.json"):
        print("ERROR: filepath 'database/events.json' not found... please check that events.json is created underneath the database folder.")
        return
    print("Ready")
    print("\n------ Goals ------\n1. newEvent = creates new event\n2. delEvent = deletes event\n3. getEvent = prints out event\n4. srcToEvent = sends contents of src.txt to json file for website publication")
    t = input("\nPlease enter goal: ")
    if t == "newEvent" or t == "1":
        print("Goal 1 Selected...\n")
        title = input("Title of Event: ")
        desc = input("Description of Event: ")
        img = input("Image link (type none if n/a): ")
        print("Creating new event...")
        if img == "" or img == "none" or img == "na":
            img = ""
        newEvent(title, desc, img)
        print("Successfully created new event!")
    elif t=="delEvent" or t == "2":
        print("Goal 2 Selected...\n")
        id = input("ID of Event: ")
        status = deleteEvent(id)
        if status:
            print("Successfully deleted event with ID of "+id)
        else:
            print("Could not find event with the id "+id)
    elif t=="getEvent" or t == "3":
        print("Goal 3 Selected...\n")
        title = input("Title of Event: ")
        status = getEventFromTitle(title)
        if status != None:
            print("Event data for ID: "+status["UUID"])
            print(status)
        else:
            print("Event not found with title '"+title+"' check spelling mistakes or capital letters")
    elif t=="srcToEvent" or t == "4":
        print("Goal 4 Selected...\n")
        id = input("ID of Event to enter HTML to: ")
        status = getEventFromID(id)
        if status != None:
            print("Transferring data from src.txt to article '"+status["eventCard"]["title"]+"'")
            with open("database\src.txt") as f:
                insertHtml(status, f.read())
        else:
            print("ERROR: Could not find event with the id "+id)
            return