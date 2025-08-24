import os, boto3
from botocore.exceptions import ClientError
from schoolia import settings


BUCKET = settings.AWS_STORAGE_BUCKET_NAME
REGION = settings.AWS_S3_REGION_NAME


s3_client = boto3.client(
    "s3",
    region_name=REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )

def upload_fileobj_to_s3(file_obj, key, content_type=None):
    """
    يرفع الملف إلى S3 ويعيد المفتاح (key) فقط
    """
    extra = {"ContentType": content_type} if content_type else {}

    # تأكد أن الستريم مفتوح من البداية
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

    # رفع الملف
    s3_client.upload_fileobj(file_obj, BUCKET, key, ExtraArgs=extra)

    return key

def public_url(key):
    """
    يبني رابط URL صحيح من المفتاح
    """
    return f"https://{BUCKET}.s3.{REGION}.amazonaws.com/{key}"

