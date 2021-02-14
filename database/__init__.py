from mongoengine import connect
from dotenv import load_dotenv
import os

# ----------
# db connect
# ----------
print('Connecting to DB')
load_dotenv()
db_connect = os.getenv('DB_CONNECT_URL')
connect('mydb', host=str(db_connect))
print('Connection successful')
