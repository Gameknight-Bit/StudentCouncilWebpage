#This script creates and manipulates .json files for responses from the contact page...

# it also stores recent user IP addresses (limiting only to 2 min cooldown)

import json
from datetime import datetime
from os.path import exists
from tabnanny import check
import uuid
import re

####################
## Data Structure ##
####################
# {
#   ["bugreports"] = {
#       BugReport(Obj)
#   },
#   ["webfeedback"] = {
#       Feedback(Obj)
#   },
#   ["stucofeedback"] = {
#       Email(Obj)
#   },
#   ["EMAILS-SENT"] = {
#       ["srhigh"] = {
#           Email(Obj)
#       },
#       ["jrhigh"] = {
#           Email(Obj)
#       },
#   },
#   ["RECENT-IPS"] = {
#       "ex.ip.add.res": timestamp,
#       "112.0.0.234": 772449522221,
#   }
# }

#Minutes between ip addresse's EMAIL
EMAILCOOLDOWN = 2
MAX_CHAR_RESPONSES = 3000
DEBUG_MODE = True #disables IP Adress Cooldown

### Helper Methods ###
def checkEmail(email):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

#########################
## Classes for Storage ##
#########################
# Bug Report Obj #
class BugReport:
    def __init__(self, content="", time=datetime.timestamp(datetime.now())):
        self.content = str(content)
        self.time = str(datetime.timestamp(datetime.now()))
        self.UUID = str(uuid.uuid4().hex)

    def __str__(self):
        return "'"+self.content+"' | @"+str(self.time+" | ID: "+str(self.UUID))

    def genUUID(self):
        id = str(uuid.uuid4().hex)
        self.UUID = id
        return id

    def todict(self):
        return {"content": self.content, "time": str(self.time), "UUID": str(self.UUID)}

    def fromdict(self, dict):
        self.content = dict["content"]
        self.time = dict["time"]

    @staticmethod #Returns True if all args are valid (else, returns string w/ error message)
    def validate(content="", time=0):
        if str(content).strip() == "":
            return "No Content Provided"
        elif float(time) < 0:
            return "Time negative"
        return True


# Feedback Obj #
class Feedback:
    def __init__(self, content="", rating="-1", time=datetime.timestamp(datetime.now())):
        self.content = str(content)
        self.rating = str(rating)
        self.time = str(datetime.timestamp(datetime.now()))
        self.UUID = str(uuid.uuid4().hex)

    def __str__(self):
        return "content: "+str(self.content)+"' | rating: "+str(self.rating)+"' | @"+str(self.time)+"' | ID: "+str(self.UUID)

    def setType(self, feedbacktype):
        self.type = str(feedbacktype)

    def getType(self):
        return self.type or ""

    def genUUID(self):
        id = str(uuid.uuid4().hex)
        self.UUID = id
        return id

    def todict(self):
        return {"rating": self.rating, "content": self.content, "time": str(self.time), "UUID": str(self.UUID)}

    def fromdict(self, dict):
        self.content = dict["content"]
        self.rating = dict["rating"]
        self.time = dict["time"]
        self.UUID = dict["UUID"]

    @staticmethod #Returns True if all args are valid (else, returns string w/ error message)
    def validate(content="", rating="-1", time=0):
        if str(content).strip() == "":
            return "No Content Provided"
        elif float(time) < 0:
            return "Time negative"
        return True

# Email Obj #
class Email:
    def __init__(self, anon=False, email="", content="", subject="No Subject", name="", rating="-1", time=datetime.timestamp(datetime.now())):
        if anon == True:
            self.email = "Anonymous@gmail.com"
            self.name = "Anonymous"
        else:
            self.email = str(email)
            self.name = str(name)
        self.subject = str(subject)
        self.content = str(content)
        self.rating = str(rating)
        self.time = str(datetime.timestamp(datetime.now()))
        self.UUID = str(uuid.uuid4().hex)

    def __str__(self):
        return "email: "+self.email+"' | name: "+str(self.name)+"' | subject: "+str(self.subject)+"' | content: "+str(self.content)+"' | rating: "+str(self.rating)+"' | @"+str(self.time)+"' | ID: "+str(self.UUID)

    def setType(self, feedbacktype):
        self.type = str(feedbacktype)

    def getType(self):
        return self.type or ""

    def genUUID(self):
        id = str(uuid.uuid4().hex)
        self.UUID = id
        return id

    def todict(self):
        return {"email": self.email, "name": self.name, "subject": self.subject, "rating": self.rating, "content": self.content, "time": str(self.time), "UUID": str(self.UUID)}

    def fromdict(self, dict):
        self.content = dict["content"]
        self.email = dict["email"]
        self.name = dict["name"]
        self.subject = dict["subject"]
        self.rating = dict["rating"]
        self.time = dict["time"]
        self.UUID = dict["UUID"]

    @staticmethod #Returns True if all args are valid (else, returns string w/ error message)
    def validate(anon=False, email="", content="", subject="No Subject", name="", rating="-1", time=0):
        if str(content).strip() == "":
            return "No Content Provided"
        elif checkEmail(email) == False:
            return "Invalid Email"
        elif float(time) < 0:
            return "Time negative"
        return True

##############################
## DATASTORE EDITOR SECTION ##
##############################
def addData(directoryName , ip, data):
    with open("database/responses.json", "r+") as f:
        d = json.load(f)
        structure = None
        weirdNamingConvention = ""

        data["content"] = (data["content"][:MAX_CHAR_RESPONSES] + '..') if len(data["content"]) > MAX_CHAR_RESPONSES else data["content"]

        if directoryName == "bugreports":
            structure = BugReport(data["content"])

        elif directoryName == "webfeedback":
            structure = Feedback(data["content"], data["rating"])

        elif directoryName == "stucofeedback":
            structure = Email(anon=data["anon"], subject=data["subject"], name=data["name"], email=data["email"], rating=data["rating"], content=data["content"])

        elif directoryName == "jrhighstuco":
            weirdNamingConvention = "jrhigh"
            structure = Email(anon=data["anon"], subject=data["subject"], name=data["name"], email=data["email"], rating=data["rating"], content=data["content"])

        elif directoryName == "srhighstuco":
            weirdNamingConvention = "srhigh"
            structure = Email(anon=data["anon"], subject=data["subject"], name=data["name"], email=data["email"], rating=data["rating"], content=data["content"])

        else:
            return "500 Internal Server Error: "+directoryName+" is not a valid choice..."

        id = structure.genUUID()
        if directoryName == "jrhighstuco" or directoryName == "srhighstuco":
            d["EMAILS-SENT"][weirdNamingConvention][id] = structure.todict()
        else:
            d[directoryName][id] = structure.todict()
        d["RECENT-IPS"][ip] = datetime.timestamp(datetime.now())
        f.seek(0)
        json.dump(d, f, indent=4)
        f.truncate()

def checkDataValidity(dName, data):
    if dName == "bugreports":
        return BugReport.validate(data["content"])

    elif dName == "webfeedback":
        return Feedback.validate(data["content"], data["rating"])

    elif dName == "stucofeedback":
        return Email.validate(anon=data["anon"], subject=data["subject"], name=data["name"], email=data["email"], rating=data["rating"], content=data["content"])

    elif dName == "jrhighstuco":
        return Email.validate(anon=data["anon"], subject=data["subject"], name=data["name"], email=data["email"], rating=data["rating"], content=data["content"])

    elif dName == "srhighstuco":
        return Email.validate(anon=data["anon"], subject=data["subject"], name=data["name"], email=data["email"], rating=data["rating"], content=data["content"])

    else:
        return "500 Internal Server Error: "+dName+" is not a valid choice..."


def checkIP(ip): #Returns True if IP is NOT on cooldown | False if Cooldown is in effect
    if DEBUG_MODE == True:
        return True

    with open("database/responses.json", "r+") as f:
        d = json.load(f)
        ips = d["RECENT-IPS"]

        index = 0
        for key, val in ips.items():
            if key == ip:
                if datetime.timestamp(datetime.now()) - float(val) < EMAILCOOLDOWN*60:
                    return False
                else:
                    ips.pop(key)
                    break
        f.seek(0)
        json.dump(d, f, indent=4)
        f.truncate()
        return True

#### SHOULD ONLY BE RAN ONCE EVER!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ####
def initDatabase():
    with open("database/responses.json", "r+") as f:
        d = json.load(f)
        
        d["bugreports"] = {}
        d["webfeedback"] = {}
        d["stucofeedback"] = {}
        d["EMAILS-SENT"] = {
            "srhigh": {},
            "jrhigh": {}
        }
        d["RECENT-IPS"] = []

        f.seek(0)
        json.dump(d, f, indent=4)
        f.truncate()
        return True

def purgeResponses(past=120):
    with open("database/responses.json", "r+") as f:
        d = json.load(f)
        ips = d["RECENT-IPS"]

        index = 0
        for key, val in ips.items():
            if datetime.timestamp(datetime.now()) - float(val) < past:
                return False
            else:
                ips.pop(key)
                break
        f.seek(0)
        json.dump(d, f, indent=4)
        f.truncate()