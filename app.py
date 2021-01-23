import pymongo
from flask import Flask, render_template, request
from flask_mongoengine import MongoEngine  # forse inutile
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange

app = Flask(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
app.config[
    "MONGO_URI"] = "mongodb+srv://dbAdmin:a7jbigFLN5Oo9HqL@clustersecondote.wdodi.mongodb.net/secondote?retryWrites=true&w=majority"

conn = pymongo.MongoClient(
    'mongodb+srv://dbAdmin:a7jbigFLN5Oo9HqL@clustersecondote.wdodi.mongodb.net/secondote?retryWrites=true&w=majority')
db = conn.SecondoTe  # SecondoTe is my database
col = db.SecondoTe  # Here SecondoTe is my collection
cur = col.find()

mongo = PyMongo(app)
 #variabili di sistema
app.domanda = ''
app.element = {}



class ToEstimateForm(FlaskForm):
    #number = FloatField('Secondo te', validators=[DataRequired(), NumberRange(min=0, max=100, message=(
    #    'Number must be between 0 and 100'))])
    number = FloatField('Secondo te', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/')
@app.route('/home')
def hello_world():
    for doc in cur:
        print(doc)
        form = ToEstimateForm(request.form)
        app.domanda = doc['secondote']
        app.element = doc
        return render_template('index.html', secondoTe=doc, form=form)



@app.route('/result', methods=['POST', 'GET'])
def result():
    app.element['risposte'] = app.element['risposte'] + 1
    app.element['media'] = app.element['sommarisposte'] + 1
    app.element['mediana'] = app.element['sommarisposte'] + 1
    app.element['moda'] = app.element['sommarisposte'] + 1
    return render_template('result.html', secondoTe=app.element, domanda=app.domanda)


if __name__ == '__main__':
    app.run()
