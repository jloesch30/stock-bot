from mongoengine import connect
import os

# ----------
# db connect
# ----------
print('Connecting to DB')
connect('mydb', host="mongodb+srv://jloesch30:NkUB2z7wxRrDdmaI@cluster0.rkkey.mongodb.net/mydb?retryWrites=true&w=majority")
print('Connection successful')
