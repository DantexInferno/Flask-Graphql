from flask import Flask
from db import init_db
from flask_graphql import GraphQLView
from schema import schema


app = Flask(__name__)
app.debug = True

app.add_url_rule(
    "/api", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
  )


if __name__ == "__main__":
  #below uncomment init_db to insert info in db
  #init_db
  app.run()
