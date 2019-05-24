from flask import Flask, request
from flask_restful import Resource, Api
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

api = Api(app)


csrf_protect = CSRFProtect(app)
api = Api(app, decorators=[csrf_protect.exempt])

mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123'
app.config['MYSQL_DATABASE_DB'] = 'asana'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

class Question(Resource):
    def get(self, question_id):
        with mysql.connect() as cursor:
            sql = "SELECT * FROM db_german WHERE id=" + question_id
            cursor.execute(sql)
            return cursor.fetchall()[0]
    
    def delete(self,question_id):
        try:
            with mysql.connect() as cursor:
                sql = "DELETE  FROM db_german WHERE id=" + question_id
                cursor.execute(sql)
                return {"data": "was deleted"}
        except:
                return {"status": "error"}

    def put(self, question_id):
        word = request.json["word"]
        theme = request.json["theme"]
        example = request.json["example"]
        level = request.json["level"]
        
        try:    
            with mysql.connect() as cursor:
                cursor.execute("""UPDATE db_german SET word=%s, theme=%s, example=%s, level=%s WHERE id=%s""",
                (word, theme, example, level, question_id))
                return {"Data": "was Updated"}
        except:
            return {"status": "error"}

class QuestionList(Resource):
    def get(self):
        with mysql.connect() as cursor:
            sql = "SELECT * FROM db_german ORDER BY id"
            cursor.execute(sql)
            return cursor.fetchall()
    
    def post(self):
        word = request.json["word"]
        theme = request.json["theme"]
        example = request.json["example"]
        level = request.json["level"]
        try:
            with mysql.connect() as cursor:
                sql = "INSERT INTO db_german (word, theme, example, level) VALUES (%s, %s, %s, %s)"
                val = (word, theme, example,level)
                cursor.execute(sql, val)
                return {"status": "Ok"}
        except:
            return {"status": "error"}
        
class QuestionListByLevel(Resource):
    def get(self, level_id):
        try:
            with mysql.connect() as cursor:
                sql = "SELECT * FROM db_german WHERE level='{}' ORDER BY RAND() LIMIT 3".format(level_id)
                cursor.execute(sql)
                return cursor.fetchall()
        except:
            return {"status": "Level error"}

api.add_resource(QuestionList, '/questions')
api.add_resource(Question, '/questions/<string:question_id>')
api.add_resource(QuestionListByLevel, '/level/<string:level_id>')


if __name__ == '__main__':
    app.run(debug=True)