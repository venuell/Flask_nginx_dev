from flask import Flask
#from flask.ext.session import Session


app= Flask (__name__)
app.config['SECRET_KEY']='jghsjhgjsdhgjshgjksh'
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
#Session(app)
#def create_app():
#    app = Flask (__name__)
#    app.config['SECRET_KEY']='jghsjhgjsdhgjshgjksh'
    #from flaskproject import routes
#    return app
from flaskproject import routes
