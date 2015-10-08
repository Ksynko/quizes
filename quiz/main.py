import sys
from flask import Flask
from flask import request, render_template
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from quiz.models import Question, db_connect, create_deals_table

app = Flask(__name__)
sys.path.append(".")

sections = ['Anatomy MCQs', 'Pathology MCQs', 'Physiology MCQs', 'Other MCQs']
categories = [
    'Multiple Choice (Type A)',
    'Multiple True/False (Type X)',
    'Relationship-Analysis (Type B)']


@app.route('/', methods=['POST', 'GET'])
def show_main():
    engine = db_connect()
    create_deals_table(engine)
    Session = sessionmaker(bind=engine)
    sess = Session()

    if request.method == 'POST':
        section = int(request.form['section'])
        category = int(request.form['category'])
        q = sess.query(Question).filter(
            Question.section == sections[section],
            Question.type_of_quiz == categories[category]
        ).order_by(func.random()).all()[:20]

        return render_template(
            'quiz_form.html',
            questions=q,
            title=sections[section]+': '+categories[category])

    else:
        return render_template('start_form.html')


@app.route('/check', methods=['POST', 'GET'])
def check_quiz():
    engine = db_connect()
    create_deals_table(engine)
    Session = sessionmaker(bind=engine)
    sess = Session()

    if request.method == 'POST':
        category = request.form['category']
        answers = {}
        correct_answers = {}
        wrong_answers = {}
        if category == categories[1]:
            for r in request.form:
                if r != 'category':
                    answers[r] = request.form.getlist(r)
            for k, v in answers.items():
                answers[k] = '.,'.join(v)
                answers[k] += '.'

            for k, v in answers.items():
                q = sess.query(Question).filter(
                    Question.question_number == k).first()

                if v == q.correct_answer:
                    correct_answers[v] = q
                else:
                    wrong_answers[v] = q
        else:
            for r in request.form:
                if r != 'category':
                    answers[r] = request.form[r]

            for k, v in answers.items():
                q = sess.query(Question).filter(
                    Question.question_number == k).first()

                if v in q.correct_answer:
                    correct_answers[v] = q
                else:
                    wrong_answers[v] = q

        return render_template(
            'results.html',
            title='Results',
            correct_answers=correct_answers,
            wrong_answers=wrong_answers)


@app.route('/tests')
def show():
    return render_template('main.html')


@app.route('/get_data')
def get_data():
    engine = db_connect()
    create_deals_table(engine)
    Session = sessionmaker(bind=engine)
    sess = Session()

    if request.method == 'GET':
        section = int(request.args.get('section'))
        category = int(request.args.get('category'))
        q = sess.query(Question).filter(
            Question.section == sections[section],
            Question.type_of_quiz == categories[category]
        ).order_by(Question.question_number).all()

        return render_template(
            'quiz.html',
            questions=q,
            title=sections[section]+': '+categories[category])


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
