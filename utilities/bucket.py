import boto3
from django.conf import settings


class Bucket:
    def __init__(self):
        session = boto3.session.Session()
        self.connection = session.client(
            service_name=settings.AWS_SERVICE_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        )

    def get_bucket_objects(self):
        objects = self.connection.list_objects_v2(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        if objects.get("KeyCount", 0) > 0:
            return objects["Contents"]
        return None

    def delete_bucket_object(self, key):
        self.connection.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                                      Key=key)
        return True

    def download_bucket_object(self, key):
        with open(settings.AWS_LOCAL_STORAGE + key, "wb") as file:
            self.connection.download_fileobj(settings.AWS_STORAGE_BUCKET_NAME,
                                             key, file)


bucket = Bucket()
