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
            math_level = form.math_level.data,
            practice_problem_one = form.practice_problem_one.data,
            practice_problem_two = form.practice_problem_two.data,
            practice_problem_three = form.practice_problem_three.data,
            solution_one = form.solution_one.data,
            solution_two = form.solution_two.data,
            solution_three = form.solution_three.data,
            topic_name = form.topic_name.data
            

        )
        newMathTopic.save()
        flash('New math topic created successfully!', 'success')
        return redirect(url_for("algebra"))
    return render_template('topic_form.html', form=form)