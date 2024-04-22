from app import app
from app.utils.secrets import getSecrets
from app.classes.forms import MathTopicForm
import requests
from flask import render_template, flash, redirect, url_for
import requests
from flask_login import current_user
from app.classes.forms import ClinicForm
from app.classes.data import newTopic, User, Clinic
from flask_login import login_required
import datetime as dt


@app.route('/mathLevel/algebra')
@login_required
def algebra():

   

    return render_template('algebra.html')

@app.route('/mathLevel/createtopic', methods=['GET', 'POST'])
@login_required

def topicForm():
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
    return render_template('topic_form.html', form=form)

@app.route('/mathLevel/algebratwo')
@login_required
def algebraTwo():

    

    return render_template('algebratwo.html')
@app.route('/mathLevel/precalculus')
@login_required
def preCalculus():

    

    return render_template('precalculus.html')

@app.route('/mathLevel/statistics')
@login_required
def statistics():

    

    return render_template('statistics.html')

@app.route('/mathLevel/geom')
@login_required
def geometry():

    

    return render_template('geom.html')


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
