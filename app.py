import pymongo
from flask import Flask, render_template, request, session
from flask_mongoengine import MongoEngine  # forse inutile
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, FloatField, StringField
from wtforms.validators import DataRequired, NumberRange
from flask_uploads import \
    UploadSet  # NB: https://stackoverflow.com/questions/61628503/flask-uploads-importerror-cannot-import-name-secure-filename
from flask_uploads import configure_uploads
from flask_uploads import IMAGES, patch_request_class
import os
from flask_bootstrap import Bootstrap
from werkzeug.datastructures import FileStorage

app = Flask(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
app.config[
    "MONGO_URI"] = 'mongodb+srv://dbAdmin:a7jbigFLN5Oo9HqL@clustersecondote.wdodi.mongodb.net/secondote?retryWrites=true&w=majority'

app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + "\static"  # for upload

conn = pymongo.MongoClient(
    'mongodb+srv://dbAdmin:a7jbigFLN5Oo9HqL@clustersecondote.wdodi.mongodb.net/secondote?retryWrites=true&w=majority')
db = conn.SecondoTe  # SecondoTe is my database
col = db.SecondoTe  # Here SecondoTe is my collection
cur = col.find()
# mongo = PyMongo(app)
# variabili di sistema
app.domanda = ''
app.elements = []
for doc in cur:
    print(doc)
    app.elements.append(doc)

# for upload image
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

Bootstrap(app)


class ToEstimateForm(FlaskForm):
    '''number = FloatField('Secondo te', validators=[DataRequired(), NumberRange(min=0, max=100, message=(
    #    'Number must be between 0 and 100'))])'''
    number = FloatField('Secondo te', validators=[DataRequired()])
    submit = SubmitField('Submit')


class NewEstimateForm(FlaskForm):
    phrase = StringField('phrase', validators=[DataRequired()])
    file = FileField('file')
    upload = SubmitField('Submit')


@app.route('/')
def hello_world():
    form = ToEstimateForm(request.form)
    return render_template('index.html', secondoTe=app.elements[0], form=form)


@app.route('/')
@app.route('/secondoTe/<idSecondoTe>')
def secondoTe(idSecondoTe=None):
    form = ToEstimateForm(request.form)
    return render_template('index.html', secondoTe=app.elements[int(idSecondoTe) - 1], form=form)


@app.route('/allSecondoTe')
def allSecondoTe():
    return render_template('allSecondoTe.html', listSecondoTe=app.elements)


@app.route('/newSecondote', methods=['GET', 'POST'])
def newSecondoTe():
    if not os.path.exists('static/imgUploaded'):
        os.makedirs('static/imgUploaded')
    form = NewEstimateForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        # TODO: handle img from form
             #filename = photos.save(form.file.data, name=str(form.phrase.data) + '.jpg', folder='imgUploaded')
        # TODO: insert new estimate to DB

        # mando la stringa con la nuova stima alla pagina confirmNewSecondoTe.html
        return render_template('confirmNewSecondoTe.html', added=form.phrase.data) # img=filename # forse meglio redirect
    return render_template('newSecondote.html', form=form)


@app.route('/confirmNewSecondoTe', methods=['GET', 'POST'])
def confirmNewSecondoTe():
    return render_template('confirmNewSecondoTe.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    app.elements[0]['risposte'] = app.elements[0]['risposte'] + 1
    app.elements[0]['media'] = app.elements[0]['sommarisposte'] + 1
    app.elements[0]['mediana'] = app.elements[0]['sommarisposte'] + 1
    app.elements[0]['moda'] = app.elements[0]['sommarisposte'] + 1
    return render_template('result.html', secondoTe=app.elements[0])


if __name__ == '__main__':
    app.run()
