#IMPORTANT: Change path to wkhtmltopdf for windows to .exe and backslash;
#There may be margin errors with the windows version, works best on MAC


#Import necessary modules
from flask import Flask, render_template, make_response, flash, redirect, url_for, request, logging
import pdfkit
from wtforms import Form, StringField, SelectField, validators, SelectMultipleField, widgets, IntegerField

#SQLAlchemy Part
#These import import the required functionality for SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

#DEclare base for SQLAlchemy
Base = declarative_base()

#Describe Spell Table
class Spell(Base):
    #Declare Tablename
	__tablename__ = "spells"

    #Declare table Columns
	id = Column('id', Integer, primary_key=True)
	name = Column('name', String, unique=True)
	level = Column('level', Integer)
	school = Column('school', String)
	verbal = Column('verbal', Boolean)
	somatic = Column('somatic', Boolean)
	material = Column('material', Boolean)
	ingredients = Column('ingredients', String)
	casting_time = Column('casting_time', String)
	range = Column('range', String)
	duration = Column('duration', String)
	description = Column('description', String)

#Describe Class Table
class Class(Base):
    #Declare Tablename
	__tablename__ = "classes"

    #Declare table Columns
	id = Column('id', Integer, primary_key=True)
	name = Column('name', String, unique=True)

#Describe Class-Spell-Linking(Csl) Table
class Csl(Base):
    #Declare Tablename
	__tablename__ = "classSpellLink"

    #Declare table Columns
	id = Column('id', Integer, primary_key=True)
	spell_id = Column('spell_id', Integer, ForeignKey("spells.id"))
	class_id = Column('class_id', Integer, ForeignKey("classes.id"))


#Create SQLAlchemy engine, create table link with the engine and build a sessionmaker
engine = create_engine('sqlite:///database/dd5.db')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)


app = Flask(__name__)

#Configure wkhtmltopdf engine path and style sheet
path_wkthmltopdf = 'venv/Include/wkhtmltopdf'
app.conf = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
app.css = 'static/style.css'

#Describe MultiCheckboxField Class for checkboxes on the website (V,S,M)
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

#Describe Queryform as the hole form presented to the user on the website
class queryform(Form):
    #Describe multiple classes choices
    multipleclasschoices = [
                ('Please choose', 'Please choose'),
                ('Warlock', 'Warlock'),
                ('Sorcerer', 'Sorcerer'),
                ('Bard', 'Bard'),
                ('Druid', 'Druid'),
                ('Paladin', 'Paladin'),
                ('Ranger', 'Ranger'),
                ('Wizard', 'Wizard'),
                ('Cleric', 'Cleric')]
    #Declare form field with described form data from multipleclasschoices
    Class = SelectField('Select Class:', choices=multipleclasschoices)
    #Declare form field Spellname
    Spellname = StringField('Spell name')
    #Declare form field that accepts the spell level from 0-9 with validators
    Spelllevel = IntegerField('Spell level (0-9)', [validators.NumberRange(message='Please enter a number between 0 and 9', min=0, max=9), validators.Optional()])
    #Describe multiple spell school choices
    spellschoolchoices = [
                ('Please choose', 'Please choose'),
                ('Abjuration', 'Abjuration'),
                ('Conrujation', 'Conjuration'),
                ('Divination', 'Divination'),
                ('Enchantment', 'Enchantment'),
                ('Evocation', 'Evocation'),
                ('Illusion', 'Illusion'),
                ('Necromancy', 'Necromancy'),
                ('Transmutation', 'Transmutation')]
    #Declare form field with described form data from spellschoolchoices
    selectspellschool = SelectField('Select Spellschool:', choices=spellschoolchoices)
    #Describe multiple check box choices (multiple can be choosen)
    multiplechoicevsm = [('Verbal', 'Verbal'),
                ('Somatic', 'Somatic'),
                ('Material', 'Material')]
    #Declare multiple choice check box field in form using descriptive data from multiplechoicevsm
    selectmultiplevsm = MultiCheckboxField('VSM', choices=multiplechoicevsm)
    

#This route trigers at the base route of the website and accepts GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def query():
    #Load queryform
    form = queryform(request.form)
    #Check if form data was posted and if the data is valid
    if request.method == 'POST' and form.validate():
        #Declare VSM variables
        sqlv = 0
        sqls = 0
        sqlm = 0

        #GEt from data and save it in variables
        sqlclass = form.Class.data
        sqlspellname = form.Spellname.data
        sqlspelllevel = form.Spelllevel.data
        sqlspellschool = form.selectspellschool.data
        sqlmultvsm = form.selectmultiplevsm.data
        #Extract VSM data out of the list sqlmultvsm
        if 'Verbal' in form.selectmultiplevsm.data:
            sqlv = 1
        if 'Somatic' in form.selectmultiplevsm.data:
            sqls = 1
        if 'Material' in form.selectmultiplevsm.data:
            sqlm = 1

        #Check if any user specific data was given, return error if not
        if sqlclass == 'Please choose' and sqlspellname == '' and sqlspelllevel is None and sqlspellschool == 'Please choose' and sqlv == 0 and sqls == 0 and sqlm == 0:
            return render_template('query.html', error='Please enter at least one value', form=form)

        #Declare SQLAlchemy querry filter tuple
        sqlafilter = ()

        #Check if custom data was given and add filter to the filter tuple sqlafilter
        if sqlclass != 'Please choose':
            sqlafilter += (Class.name == sqlclass,)
        if sqlspellname != '':
            sqlafilter += (Spell.name.like('%' + sqlspellname + '%'),)
        if sqlspelllevel != None:
            sqlafilter += (Spell.level == sqlspelllevel,)
        if sqlspellschool != 'Please choose':
            sqlafilter += (Spell.school == sqlspellschool,)
        if sqlv != 0:
            sqlafilter += (Spell.verbal == sqlv,)
        if sqls != 0:
            sqlafilter += (Spell.somatic == sqls,)
        if sqlm != 0:
            sqlafilter += (Spell.material == sqlm,)


        #Get a SQLAlchemy session with the above generated sessionmaker
        session = Session()
        #Querry Database with SQLAlchemy for Spell with base of Csl inserting Spell and Class on id match and then apply filter and store results in a variable
        sqlquerry = session.query(Spell).select_from(Csl).join(Spell, Csl.spell_id == Spell.id).join(Class, Csl.class_id == Class.id).filter(*sqlafilter).all()
        #Close the SQLAlchemy session
        session.close()


        #Check if result is empty, proceed if not
        if sqlquerry:
            
            #Render html site with the querry results to get raw html into the variable rendered
            rendered = render_template('qres.html',sqlq=sqlquerry)
            #Generate the PDF for the user using the wkhtmltopdf engine with the raw html data, the preconfigured stylesheet and the path to the wkhtmltopdf engine
            pdf = pdfkit.from_string(rendered, False, css=app.css, configuration=app.conf)

            #Set headers to tell browser to render page as html
            response = make_response(pdf)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

            #Return PDF to user
            return response
        
        else:
            #Return error if no results were found in the Database
            return render_template('query.html', error='No results', form=form)

    #Render the query form if request type was GET and no data was POSTed
    return render_template('query.html', form=form)


#Run file if directly called
if __name__ == '__main__':
    #Run flask in debug mode
    app.run(debug=True)