from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=True)
    description = db.Column(db.String(100000),nullable=False)
    date_created = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f" {self.sno} - {self.title} "

@app.route('/',methods=['GET',"POST"])
def index():
    if request.method == "POST":
        title = request.form['title']
        description = request.form['desc']
        todo = Todo(title=title, description=description)
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    
    return render_template('index.html',alltodo=alltodo)

@app.route('/completed/<int:sno>')
def completed(sno):
    req_todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(req_todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method == "POST":
        title = request.form['title']
        description = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.description = description
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    req_todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=req_todo)


if __name__ == '__main__':
    app.run(debug=False)