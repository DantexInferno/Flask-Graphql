from mongoengine import Document
from mongoengine.fields import (
    StringField, ListField
)

class Students(Document):
  meta = {"collection": "students"}
  name = StringField()
  email = StringField()
  phone = StringField()
  avatar = StringField()


class Courses(Document):
  meta = {"collection": "courses"}
  title = StringField()
  teacher = StringField()
  description = StringField()
  topic = StringField()
  people = ListField(default=None)
  level = StringField()