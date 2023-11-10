from flask import Flask, render_template, request
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='crime_portal'
mysql= MySQL(app)

@app.route('/')
def index():
    first="Nathan"
    last="Nathan"
    pw="123"
    cur=mysql.connection.cursor()
    cursor.executue("INSERT INTO police(Fname,Lname,password) VLAUES (%s, %s, %s)",(first,last,pw))
    mysql.connection.commit()
    cur.close()
    return "SUCCESS"



if __name__ == '__main__':
    app.run(debug=True)