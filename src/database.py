import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class FirestoreDB:
    _instance = None  # Class attribute to hold the single instance

    def __new__(cls):
        """Override __new__ to control the creation of new instances."""
        if cls._instance is None:
            cls._instance = super(FirestoreDB, cls).__new__(cls)
            cls._initialize(cls._instance)
        return cls._instance

    @classmethod
    def _initialize(cls, instance):
        """Initialize the single instance."""
        cred = credentials.Certificate('credentials.json')
        firebase_admin.initialize_app(cred)
        instance.db = firestore.client()

    def save_data(self, collection, document_id, data):
        """Save data to the specified Firestore collection."""
        doc_ref = self.db.collection(collection).document(document_id)
        doc_ref.set(data)

    def get_data(self, collection):
        """Retrieve data from the specified Firestore collection."""
        docs = self.db.collection(collection).stream()
        return {doc.id: doc.to_dict() for doc in docs}