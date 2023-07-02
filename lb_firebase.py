import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# py datetime for timestamp
from datetime import date,datetime

# time and date stuff and rearranging it
today = date.today()
date = today.strftime("%d-%b-%Y")

now = datetime.now()
timeRN = now.strftime("%H:%M:%S")

# Location of the service account key (JSON file contents)
cred = credentials.Certificate('food-for-dirt-testbed-firebase-adminsdk-jqk5x-108540edd9.json')

# Intialize the app with a server account, granting admin privilages
firebase_admin.initialize_app(cred)

# makes a shortcut for typing firestore.client() as db.WatevaFirestoreCommand
db=firestore.client()
    

def firebase_deposit(userId, lockerId):

    # add firebase stuff to execute here
    print("Firebase stuff to excute ")
    print("passed data (temp_fb file): " + userId , lockerId)


    """#     ----TESTED WORKING REMOVE THIS LINE TO MAKE ACTIVE-----
    #creates document for each deposit and adds it to deposit collection in firestore
    user = str(userId)
    locker = str(lockerId)
    data = {'date' : str(today), 'time' : str(timeRN), 'locker' : str(locker), 'userId' : str(user) }
    # sends the create to firebase
    db.collection('deposit').add(data)
    """#     ----TESTED WORKING REMOVE THIS LINE TO MAKE ACTIVE-----
        