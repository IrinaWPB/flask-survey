from urllib import response
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
debug = DebugToolbarExtension


@app.route('/')
def start_page():
    """Shows title of th survey with instructions"""
    
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('index.html', 
        title = title, 
        instructions = instructions)

@app.route('/start_session', methods=["POST"])
def start_session():
    session['responses'] = []
    return redirect('/questions/0')

@app.route('/questions/<int:quest_id>')
def question(quest_id):
    """Shows question and answer options"""

    number_of_questions = len(satisfaction_survey.questions)

    if len(session['responses']) == number_of_questions:
        flash('You already answered all the questions')
        return redirect('/thankyou')

    if quest_id > len(session['responses']) or quest_id >= number_of_questions:
        quest_id = len(session['responses'])
        flash('You are trying to visit invalid page. Please answer the question')
        return redirect(f'/questions/{quest_id}')

    question = satisfaction_survey.questions[quest_id].question    
    return render_template('question_form.html', 
        question = question, 
        quest_id = quest_id,
        number_of_questions = number_of_questions,
    )

@app.route('/answer', methods=["POST"])
def answer():
    """Add user's answers to the responses list"""
    answer = request.form['choice']
    quest_id = int(request.form['quest_id'])
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses
    if len(session['responses']) == len(satisfaction_survey.questions):
        return redirect('/thankyou')
    return redirect(f'/questions/{quest_id+1}')

@app.route('/thankyou')
def thankyou_view():
    """Thank you page"""

    return render_template('thankyou.html')