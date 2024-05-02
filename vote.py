import streamlit as st

import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials


cert = {
    "type": "service_account",
    "project_id": "solar-storm-store",
    "private_key_id": st.secrets["FIRESTORE_PRIVATE_KEY_ID"],
    "private_key": st.secrets["FIRESTORE_PRIVATE_KEY"],
    "client_email": "firebase-adminsdk-w817x@solar-storm-store.iam.gserviceaccount.com",
    "client_id": "118195227691959212835",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-w817x%40solar-storm-store.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com",
}

if not firebase_admin._apps:
    cred = credentials.Certificate(cert)
    firebase_admin.initialize_app(cred)


# Initialize the Firestore client
db = firestore.client()
ID = "follow-up-votes"  # or any other fixed ID


def thumbs_up(id=ID):
    global ID
    doc_ref = db.collection("votes").document(ID)
    doc = doc_ref.get()
    vote_count = 0
    if doc.exists and "thumbs_up" in doc.to_dict():
        vote_count = int(doc.get("thumbs_up"))
    doc_ref.set({"thumbs_up": vote_count + 1}, merge=True)


def thumbs_down(id=ID):
    global ID
    doc_ref = db.collection("votes").document(ID)
    doc = doc_ref.get()
    vote_count = 0
    # Check if thums_down field exists
    if doc.exists and "thumbs_down" in doc.to_dict():
        vote_count = int(doc.get("thumbs_down"))
    doc_ref.set({"thumbs_down": vote_count + 1}, merge=True)


def get_votes(id=ID):
    global ID
    doc_ref = db.collection("votes").document(ID)
    doc = doc_ref.get()
    return doc.to_dict()


if __name__ == "__main__":
    # test to add a new article
    thumbs_up()
    thumbs_down()
    thumbs_up()
    thumbs_up()
    print(get_votes())
