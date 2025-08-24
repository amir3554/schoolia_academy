import os, boto3
from botocore.exceptions import ClientError
from schoolia import settings


BUCKET = settings.AWS_STORAGE_BUCKET_NAME
REGION = settings.AWS_S3_REGION_NAME



def upload_fileobj_to_s3(file_obj, key, content_type=None):
    s3_clent = boto3.client(
    "s3",
    region_name=REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    extra = {"ContentType": content_type} if content_type else {}

    if hasattr(file_obj, "seek"):
        try:
            file_obj.seek(0)
        except Exception:
            pass
    if hasattr(file_obj, "open"):
        try:
            file_obj.open()
        except Exception:
            pass
    s3_clent.upload_fileobj(file_obj, BUCKET, key, ExtraArgs=extra)


def public_url(key):
    return f"https://{BUCKET}.s3.{REGION}.amazonaws.com/{key}"
