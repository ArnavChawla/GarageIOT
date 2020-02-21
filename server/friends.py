import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from Flask import flask


# uid = received as parameter in endpoint
#name = recieved as parameter in Endpoints
#plate = received as parameter

def main():
    cred = credentials.Certificate("C:\\Users\\bmcla\\Documents\\GitHub\\garage\\server\\keys\\garage_firebase_key.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://garage-f4c99.firebaseio.com/'
    })

    db = firestore.client()

    friends = db.collection(u'users').document(str(uid)).collection(u'friends')

    new_friend = friends.document(str(plate)).set({
        'name' : str(name)
    })
