import os
import re
import boto3
from flask import flash

ID = "id"
NAME = "name"

def s3_client():
    session = boto3.session.Session() 
    client = session.client(
        "s3", 
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
    return client

class Image:

    @classmethod
    def upload_image_to_s3(cls, file, filename):

        s3_client().upload_fileobj(file, "next-nursery", filename)