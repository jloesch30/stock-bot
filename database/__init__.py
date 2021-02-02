from mongoengine import connect
import os

# ----------
# db connect
# ----------
print('Connecting to DB')
db = connect('stock-bot-db', host=os.getenv('DB_CONNECT_URL'))
print('Connection successful')
