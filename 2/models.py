from mongoengine import Document, StringField, BooleanField

class Contact(Document):
    full_name = StringField(required=True, max_length=100)
    email = StringField(required=True, max_length=100)
    sent_email = BooleanField(default=False)
    