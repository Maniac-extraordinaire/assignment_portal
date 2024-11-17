from mongoengine import Document, StringField, BooleanField, ReferenceField, DateTimeField
from datetime import datetime

# Create your models here.

class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    is_admin = BooleanField(default=False)

class Assignment(Document):
    user = ReferenceField(User, required=True)  # Who uploaded the assignment
    task = StringField(required=True)
    admin = ReferenceField(User, required=True)  # Admin assigned to review
    status = StringField(default="Pending")  # Status: Pending, Accepted, Rejected
    timestamp = DateTimeField(default=datetime.now)  # Upload time