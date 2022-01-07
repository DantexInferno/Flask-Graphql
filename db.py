from mongoengine import connect

from models import Students, Courses

# common connection
connect(host='mongodb://localhost:host/collection_name')
#if connection has a user
#connect(host='mongodb://user:pass@localhost:host/collection_name')


def init_db():
    # Create the fixtures
    student = Students(name='peter', email='peter@gmail.com')
    student.save()

    course = Courses(title='prueba 5', teacher='jim', description='young teacher', topic='laws')
    course.save()