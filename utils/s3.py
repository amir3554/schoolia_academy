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
    extra = {}
    if content_type:
        extra["ContentType"] = content_type
        extra['ACL'] = 'public-read'
    # لا ترسل ACL إذا كان البكت مفعّل فيه Bucket owner enforced (الافتراضي اليوم)
    try:
        s3_clent.upload_fileobj(file_obj, BUCKET, key, ExtraArgs=extra)
    except ClientError as e:
        # رجّع سبب الخطأ للتشخيص
        raise RuntimeError(f"S3 upload failed: {e}")

def public_url(key):
    return f"https://{BUCKET}.s3.{REGION}.amazonaws.com/{key}"
