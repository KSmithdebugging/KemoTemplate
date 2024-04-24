from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user
from app import app
from app.classes.data import MathTopic, User
from app.classes.forms import MathTopicForm
from flask_login import login_required


@app.route('/math_topic/new', methods=['GET', 'POST'])
@login_required
def newTopic():
    form = MathTopicForm()
    if form.validate_on_submit():
        print("Form data:", form.data)
        newMathTopic = MathTopic(
            mathLevel = form.math_level.data,
            practiceProblemOne = form.practice_problem_one.data,
            practiceProblemTwo = form.practice_problem_two.data,
            practiceProblemThree = form.practice_problem_three.data,
            solutionOne = form.solution_one.data,
            solutionTwo = form.solution_two.data,
            solutionThree = form.solution_three.data,
            topicName = form.topic_name.data,
            tutorialVideo = form.tutorial_video.data,
            newMathTopic =  form.topic_name.data
            

        )
        newMathTopic.save()
        flash('New math topic created successfully!', 'success')
        return redirect(url_for("algebra"))
    return render_template('topic_form.html', form=form)