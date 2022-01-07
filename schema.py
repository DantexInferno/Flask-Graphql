import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from models import Students as StudentsModel, Courses as CoursesModel
from bson.json_util import dumps

#inputs
class Students(MongoengineObjectType):
  class Meta:
    model = StudentsModel
    interfaces = (Node, )


class Courses(MongoengineObjectType):
  class Meta:
    model = CoursesModel
    interfaces = (Node, )

#Mutations
class AddStudentToCourse(graphene.Mutation):
  id_student = graphene.ID()
  id_course = graphene.ID()

  class Arguments:
    id_student = graphene.ID()
    id_course = graphene.ID()

  def mutate(self, info, **kwargs):
    id_student = kwargs.get("id_student", None)
    id_course = kwargs.get("id_course", None)
    #topeople = []
    student_to_course = {}
    student = list(StudentsModel.objects(id=id_student))
    for x in student:
      student_to_course["id"] = x["id"]
      student_to_course["name"] = x["name"]
      student_to_course["email"] = x["email"]
#    topeople.append(student_to_course)
    inpeople = CoursesModel.objects(id = id_course).update_one(push__people = student_to_course, upsert = True)
    print("here", inpeople)
    return AddStudentToCourse(
      id_student = True
    )

class CreateStudent(graphene.Mutation):

  id = graphene.ID()
  name = graphene.String()
  email = graphene.String()

  class Arguments:
    name = graphene.String(required=True)
    email = graphene.String(required=True)

  def mutate(self, info, name, email):
    student = StudentsModel(name=name, email=email)
    student.save()

    return CreateStudent(
      id = student.id,
      name = student.name,
      email = student.email
    )

class CreateCourse(graphene.Mutation):
  
  id = graphene.ID()
  teacher = graphene.String()
  title = graphene.String()
  topic = graphene.String()

  class Arguments:
    teacher = graphene.String(required=True)
    title = graphene.String(required=True)
    topic = graphene.String(required=True)

  def mutate(self, info, teacher, title, topic):
    course = CoursesModel(teacher=teacher, title=title, topic=topic)
    course.save()

    return CreateCourse(
      id = course.id,
      teacher = course.teacher,
      title = course.title,
      topic = course.topic
    )

class DeleteStudent(graphene.Mutation):
  
  ok = graphene.Boolean()

  class Arguments:
      id = graphene.ID()

  def mutate(self, info, **kwargs):
    id = kwargs.get('id', None)
    student = StudentsModel.objects(id=id)
    student.delete()
    
    return DeleteStudent(
      ok = True
    )

class DeleteCourse(graphene.Mutation):
  
  ok = graphene.Boolean()

  class Arguments:
      id = graphene.ID()

  def mutate(self, info, **kwargs):
    id = kwargs.get('id', None)
    course = CoursesModel.objects(id=id)
    course.delete()
    
    return DeleteCourse(
      ok = True
    )

#resolver mutation
class Mutation(graphene.ObjectType):
  create_student = CreateStudent.Field()
  delete_student = DeleteStudent.Field()
  add_student_to_course = AddStudentToCourse.Field()
  create_course = CreateCourse.Field()
  delete_course = DeleteCourse.Field()

#resolver query
class Query(graphene.ObjectType):
  node = Node.Field()
  all_courses = graphene.List(Courses)
  all_students = graphene.List(Students)
  get_student = graphene.List(Students, id = graphene.ID())
  get_course = graphene.List(Courses, id = graphene.ID())

  def resolve_all_students(self, info):
    return list(StudentsModel.objects.all())

  def resolve_all_courses(self, info):
    return list(CoursesModel.objects.all())

  def resolve_get_student(self, info, **kwargs):
    id = kwargs.get("id", None)
    student =  list(StudentsModel.objects(id = id))
    if student:
      return student
        
    return []

  def resolve_get_course(self, info, **kwargs):
    id = kwargs.get("id", None)
    course =  list(CoursesModel.objects(id = id))
    if course:
      return course
        
    return []
    

schema = graphene.Schema(query=Query, types=[Students, Courses], mutation=Mutation)