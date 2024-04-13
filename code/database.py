import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class FirestoreDB:
    def __init__(self):
        cred = credentials.Certificate('credentials.json')
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def save_data(self, collection, document_id, data):
        doc_ref = self.db.collection(collection).document(document_id)
        doc_ref.set(data)

    def get_data(self, collection):
        docs = self.db.collection(collection).stream()
        return {doc.id: doc.to_dict() for doc in docs}
