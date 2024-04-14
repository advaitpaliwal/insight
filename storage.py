from google.cloud import storage
from vars import STORAGE_CREDENTIALS_FILE


class GCStorage:
    def __init__(self):
        self.client = storage.Client.from_service_account_json(
            STORAGE_CREDENTIALS_FILE)
        self.bucket = self.client.bucket("mhacks-data")

    def upload_file(self, key, file_path, public=True, content_disposition='inline'):
        blob = self.bucket.blob(key)
        blob.content_disposition = content_disposition
        blob.upload_from_filename(file_path)
        if public:
            self.make_blob_public(blob)
        return blob.public_url

    def make_blob_public(self, blob):
        policy = blob.bucket.get_iam_policy(requested_policy_version=3)
        policy.bindings.append({
            'role': 'roles/storage.objectViewer',
            'members': {'allUsers'}
        })
        blob.bucket.set_iam_policy(policy)

    def list_files(self):
        blobs = self.bucket.list_blobs()
        return [blob.name for blob in blobs]

    def retrieve_file(self, key, download_path):
        blob = self.bucket.blob(key)
        blob.download_to_filename(download_path)

    def delete_file(self, key):
        blob = self.bucket.blob(key)
        blob.delete()

    def get_public_url(self, key):
        return f"https://storage.googleapis.com/{self.bucket.name}/{key}"


if __name__ == "__main__":
    store = GCStorage()
    print(store.list_files())
    store.upload_file("test.txt", "test.txt")
    print(store.list_files())
    store.delete_file("test.txt")
    print(store.list_files())
    print(store.get_public_url("test.txt"))
