###########################
## STUCO WEBPAGE BACKEND ##
###########################

# Notes for Dev:
#Run venv\Scripts\activate.bat in CMD!!! (Then install :))#

## Imports ##
#from curses.ascii import isdigit
from flask import Flask, render_template, redirect, url_for, request, session

# File Imports #
from events import getEvents
import responses
#############

## Constants ##
HOMEPAGEIMGLINKS = ["https://3.files.edl.io/8b01/21/10/06/160344-a5ced8d0-3b57-4893-8241-6e0b423b1593.JPG",
                    "https://3.files.edl.io/569e/21/10/06/160217-967b7c42-60db-477e-b822-0b8c6ddeff96.JPG",
                    "https://3.files.edl.io/09bb/21/10/06/160447-8c87b633-d5d2-401b-89ee-cf3a0110cc28.JPG"
                   ]

app = Flask(__name__, static_url_path="/static") #Default behavior :)

@app.route('/')
def home():
    return render_template("homepage.html", data=HOMEPAGEIMGLINKS, events=getEvents())

@app.route('/about')
def about():
  return render_template("about.html")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  errmsg = ""
  validmsg = ""
  if request.method == "POST":
    email = request.form['email']
    subject = request.form['subject']
    nickname = request.form['nickname']
    content = request.form['emailContent']
    print(content)
    rating = request.form['rating']
    if rating.isdigit():
      rating = int(rating)
    else:
      rating = -1

    contactType = str(request.form["contactMethod"])
    if contactType == "-- Choose Contact Method --":
      errmsg = "Please choose a contact method before submitting feedback!"
      return render_template("contact.html", invalidText=errmsg)

    anon = request.form.get("anonymousCheck")
    anon = (anon == "on")

    print(anon)
    print(email)
    print(contactType)

    ####################### CHANGE THIS IP METHOD WHEN USING NGINIX PROXIES!!!! ##########################

    if responses.checkIP(str(request.remote_addr)):
      validmsg = "Feedback successfully recorded!"
      dataArr = {"email": str(email), "subject": str(subject), "name": str(nickname), "rating": str(rating), "content": str(content), "anon": anon}

      result = responses.checkDataValidity(contactType, dataArr)
      if result == True:
        responses.addData(contactType, str(request.remote_addr), dataArr)
      else:
        errmsg = "ERROR: Input validity error... '"+result+"'"
    else:
      errmsg = "Cooldown of 2 minutes for your IP Adress is in effect... Please wait before giving more feedback..."

    print(errmsg)
    print(validmsg)
    return redirect(url_for('contact'))

  if errmsg != "":
    print(errmsg)
    return render_template("contact.html", invalidText=errmsg)
  elif validmsg != "":
    print(validmsg)
    return render_template("contact.html", validText=validmsg)
  else:
    return render_template("contact.html")

@app.route('/events')
def events():
  return render_template("events.html", events=getEvents())

@app.route('/events/<string:uuid>')
def event(uuid):
  event = events.getEventFromID(uuid)
  if event != None:
    #eventsrc=event["source"]
    with open("database\src.txt") as f:
      data = f.read()
    return render_template("event.html", eventsrc=event["source"], title=event["eventCard"]["title"], date=event["date"], author=event["author"])
  else:
    return render_template("error.html", error="Error 404: Page Not Found", desc="This event has either been removed or never created")

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=81, debug = True) #Change when deploying :)