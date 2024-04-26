from app import app
from app.utils.secrets import getSecrets
from app.classes.forms import MathTopicForm
import requests
from flask import render_template, flash, redirect, url_for, request
import requests
from flask_login import current_user
from app.classes.forms import ClinicForm, MathTopicForm
from app.classes.data import User, Clinic, newTopic
from flask_login import login_required
import secrets
from pymongo import MongoClient
import datetime as dt
from pytube import YouTube
from bson import ObjectId

secrets = getSecrets()
client = MongoClient(secrets['MONGO_HOST'])
db = client[secrets['MONGO_DB_NAME']]
collection = db["new_topic"]
DEFAULT_THUMBNAIL_URL = "/static/default.jpg"

def retrieveTopics():
    topics = []
    data = list(collection.find().limit(9))
    for item in data:
        if 'tutorialVideo' in item:
            youtube_url = item['tutorialVideo']
            try:
                yt = YouTube(youtube_url)
                thumbnail_url = yt.thumbnail_url
                item['thumbnail_url'] = thumbnail_url
            except Exception as e:
                print(f"Error extracting thumbnail for {youtube_url}: {e}")
                item['thumbnail_url'] = DEFAULT_THUMBNAIL_URL
    print(data)
    return data


@app.route('/mathLevel/algebra', methods=['GET'])
@login_required
def algebra():
    foundTopics = retrieveTopics()
    return render_template('algebra.html', foundTopics = foundTopics)

@app.route('/mathLevel/topics', methods=['GET', 'POST'])
@login_required
def topics():
    topic = []
    document_id = request.args.get('id')
    topic = collection.find_one({'_id': ObjectId(document_id)})
    item_id = request.args.get('id')
    form_errors = None
    # Check input answers after submitting a POST request before redirecting
    if request.method == 'POST':
        first_solution =  request.form.get('1stSolution')
        second_solution =  request.form.get('2ndSolution')
        third_solution = request.form.get('3rdSolution')
        if first_solution != topic.get('solutionOne'):
            print(first_solution)
            print(topic.get('solutionOne'))
            form_errors = True
            flash('First answer is wrong!')
        elif second_solution != topic.get('solutionTwo'):
            flash('Second answer is wrong!')
            form_errors = True
        elif third_solution != topic.get('solutionThree'):
            flash('Third answer is wrong!')
            form_errors = True
        else:
            flash('New Topic Learned!', 'success')
            return render_template('index.html', form_submitted=True)
    return render_template('topics.html', data=[topic])
    

@app.route('/mathLevel/createtopic', methods=['GET', 'POST'])
@login_required

def topicForm():
    form = MathTopicForm()
    if form.validate_on_submit():
        print("Form data:", form.data)
        newMathTopic = newTopic(
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

@app.route('/mathLevel/algebratwo')
@login_required
def algebraTwo():
    foundTopics = retrieveTopics()
    

    return render_template('algebratwo.html', foundTopics = foundTopics)
@app.route('/mathLevel/precalculus')
@login_required
def preCalculus():
    foundTopics = retrieveTopics()
    

    return render_template('precalculus.html', foundTopics = foundTopics)

@app.route('/mathLevel/statistics')
@login_required
def statistics():
    foundTopics = retrieveTopics()
    

    return render_template('statistics.html', foundTopics = foundTopics)

@app.route('/mathLevel/geom')
@login_required
def geometry():
    foundTopics = retrieveTopics()
    

    return render_template('geom.html', foundTopics = foundTopics)


@app.route('/clinic/<clinicID>')
@login_required
def clinic(clinicID):

    thisClinic = Clinic.objects.get(id=clinicID)

    return render_template('clinic.html',clinic=thisClinic)


@app.route('/clinic/delete/<clinicID>')
@login_required
def clinicDelete(clinicID):
    deleteClinic = Clinic.objects.get(id=clinicID)

    deleteClinic.delete()
    flash('The Clinic was deleted.')
    return redirect(url_for('clinicList'))

def updateLatLon(clinic):
    # get your email address for the secrets file
    secrets=getSecrets()
    # call the maps API with the address
    url = f"https://nominatim.openstreetmap.org/search?street={clinic.streetAddress}&city={clinic.city}&state={clinic.state}&postalcode={clinic.zipcode}&format=json&addressdetails=1&email={secrets['MY_EMAIL_ADDRESS']}"
    # get the response from the API
    r = requests.get(url)
    # Find the lat/lon in the response
    try:
        r = r.json()
    except:
        flash("unable to retrieve lat/lon")
        return(clinic)
    else:
        if len(r) != 0:
            # update the database
            clinic.update(
                lat = float(r[0]['lat']),
                lon = float(r[0]['lon'])
            )
            flash(f"clinic lat/lon updated")
            return(clinic)
        else:
            flash('unable to retrieve lat/lon')
            return(clinic)

@app.route('/clinic/new', methods=['GET', 'POST'])
@login_required
def clinicNew():
    form = ClinicForm()

    if form.validate_on_submit():

        newClinic = Clinic(
            name = form.name.data,
            streetAddress = form.streetAddress.data,
            city = form.city.data,
            state = form.state.data,
            zipcode = form.zipcode.data,
            description = form.description.data,
            author = current_user.id,
            modifydate = dt.datetime.utcnow,
        )
        newClinic.save()

        newClinic = updateLatLon(newClinic)

        import requests

        return redirect(url_for('clinic',clinicID=newClinic.id))

    return render_template('clinicform.html',form=form)

@app.route('/clinic/edit/<clinicID>', methods=['GET', 'POST'])
@login_required
def clinicEdit(clinicID):
    editClinic = Clinic.objects.get(id=clinicID)

    if current_user != editClinic.author:
        flash("You can't edit a post you don't own.")
        return redirect(url_for('clinic',clinicID=clinicID))

    form = ClinicForm()
    if form.validate_on_submit():
        editClinic.update(
            name = form.name.data,
            streetAddress = form.streetAddress.data,
            city = form.city.data,
            state = form.state.data,
            zipcode = form.zipcode.data,            
            description = form.description.data,
            modifydate = dt.datetime.utcnow,
        )
        editClinic = updateLatLon(editClinic)
        return redirect(url_for('clinic',clinicID=clinicID))

    form.name.data = editClinic.name
    form.streetAddress.data = editClinic.streetAddress
    form.city.data = editClinic.city
    form.state.data = editClinic.state
    form.zipcode.data = editClinic.zipcode
    form.description.data = editClinic.description

    return render_template('clinicform.html',form=form)
