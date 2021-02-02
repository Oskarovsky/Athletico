import time
from datetime import timedelta
from uuid import uuid4

import firebase_admin
from firebase_admin import firestore, credentials

__all__ = ['send_to_firebase', 'update_firebase_snapshot']

# initialize_app()

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
firestore_db = firestore.client()


def send_to_firebase(raw_notification):
    db = firestore.client()
    start = time.time()
    db.collection('notifications').document(str(uuid4())).create(raw_notification)
    end = time.time()
    spend_time = timedelta(seconds=end - start)
    return spend_time


def update_firebase_snapshot(snapshot_id):
    start = time.time()
    db = firestore.client()
    db.collection('notifications').document(snapshot_id).update(
        {'is_read': True}
    )
    end = time.time()
    spend_time = timedelta(seconds=end - start)
    return spend_time


def add_exercise():
    firestore_db.collection(u'exercise').add({'type': 'twisted crunches', 'weight': 7.5,
                                              'amount': 30, 'date': time.time()})

#
# def add_new_ex(exercise):
#     firestore_db.collection(u'exercise').add({'type': ex_type, 'weight': weight,
#                                               'repetitions': amount})
