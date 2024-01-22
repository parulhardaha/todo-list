from flask import Flask, flash, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)

class Todo(db.Model):
   sno=db.Column(db.Integer, primary_key=True, autoincrement=True)
   title=db.Column(db.String(200), nullable=False)
   desc=db.Column(db.String(500))
   date_created=db.Column(db.DateTime, default=datetime.utcnow)

   def __reper__(self)-> str:
      return f"{self.sno}-{ self.title}"

@app.route('/')
def home():
    allTodo=Todo.query.all()
    print("allTodo", allTodo)
    return render_template('index.html', allTodo=allTodo)

@app.route('/add',methods=['GET','POST'])
def add():
    if request.method=='POST':
       title=request.form['title']
       desc=request.form['desc']
    if title == "" or title == None:
       flash('Unable to add a ToDo')
       return redirect("/")
    todo=Todo(title=title,desc=desc)
    db.session.add(todo)
    db.session.commit()
    flash('Sucessfully added your task!','success')
    return redirect("/")

@app.route('/update/<int:sno>')
def update(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todoValue=todo)

@app.route('/updated/<int:sno>', methods=['GET','POST'])
def updated(sno):
    title=request.form['title']
    desc=request.form['desc']
    todo=Todo.query.filter_by(sno=sno).first()
    todo.title = title
    todo.desc = desc
    db.session.add(todo)
    db.session.commit()
    flash('Successfully updated your task!','success')
    return redirect("/")

@app.route('/delete/<int:sno>')
def delete(sno ):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    flash('Successfully deleted your task!','danger')
    return redirect("/")

@app.route('/drop_all')
def drop_all():
    db.drop_all()
    db.create_all()
    return "successfully reset table"

if __name__=="__main__":
 app.run(debug=True)

   
