from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///question.db'  # SQLite database
db = SQLAlchemy(app)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(300), nullable=False)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

@app.route('/')
def home():
    questions = Question.query.all()
    return render_template('home.html', questions=questions)

@app.route('/ask', methods=['GET', 'POST'])
def ask_question():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_question = Question(title=title, content=content)
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('ask_question.html')

@app.route('/question/<int:question_id>')
def view_question(question_id):
    question = Question.query.get_or_404(question_id)
    answers = Answer.query.filter_by(question_id=question_id)
    return render_template('view_question.html', question=question, answers=answers)

@app.route('/answer/<int:question_id>', methods=['POST'])
def post_answer(question_id):
    content = request.form['content']
    new_answer = Answer(content=content, question_id=question_id)
    db.session.add(new_answer)
    db.session.commit()
    return redirect(url_for('view_question', question_id=question_id))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
