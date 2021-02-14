from mongoengine import connect
from dotenv import load_dotenv
from boto.s3.connection import S3Connection
import os

# ----------
# db connect
# ----------
print('Connecting to DB')
load_dotenv()
s3 = S3Connection(os.environ['DB_CONNECT_URL'])
db_connect = os.getenv('DB_CONNECT_URL')
connect('mydb', host=str(db_connect))
print('Connection successful')
