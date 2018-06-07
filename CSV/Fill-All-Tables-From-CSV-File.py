#Import basic functions
import csv
import os

#Import the required sqlalchemy functions
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

#Declare the database structure
class Spell(Base):
	__tablename__ = "spells"

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

class Class(Base):
	__tablename__ = "classes"

	id = Column('id', Integer, primary_key=True)
	name = Column('name', String, unique=True)

class CSL(Base):
	__tablename__ = "classSpellLink"

	id = Column('id', Integer, primary_key=True)
	spell_id = Column('spell_id', Integer)
	class_id = Column('class_id', Integer)

#Setup SQLAlchemy
engine = create_engine('sqlite:///dd5.db')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)


#Declare the spells array
spells = []
#Setting for excluding first line of csv file
firstlineofcvsisnotvalid = 1 #1 = True, 0 = False IMPORTANT

#Iterate over csv files in folder
directory = os.getcwd()
for filename in os.listdir(directory):
	if filename.endswith(".csv"):
		with open(filename, newline='', encoding='mac_roman',) as csvfile: #The encoding is required on mac for the programm to be able to read UNICODE, remove it on windows if not needed.
			csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
			#Depends on setting
			if firstlineofcvsisnotvalid == 1:
				next(csvreader, None)

			#Iterate over rows in csv file, add the line to a library and save the libraries in the 'spells' array
			for row in csvreader:
				spell = {}

				spell['class'] = filename.replace('.csv', '')
				spell['name'] = row[2]
				spell['level'] = int(row[1])

				if 'Abjuration' in row[3]:
					spell['school'] = 'Abjuration'
				if 'Conjuration' in row[3]:
					spell['school'] = 'Conjuration'
				if 'Divination' in row[3]:
					spell['school'] = 'Divination'
				if 'Enchantment' in row[3]:
					spell['school'] = 'Enchantment'
				if 'Evocation' in row[3]:
					spell['school'] = 'Evocation'
				if 'Illusion' in row[3]:
					spell['school'] = 'Illusion'
				if 'Necromancy' in row[3]:
					spell['school'] = 'Necromancy'
				if 'Transmutation' in row[3]:
					spell['school'] = 'Transmutation'
				

				if 'V' in row[6]:
					spell['verbal'] = 1
				else:
					spell['verbal'] = 0
				if 'S' in row[6]:
					spell['somatic'] = 1
				else:
					spell['somatic'] = 0
				if 'M' in row[6]:
					spell['material'] = 1
					spell['ingredients'] = row[8][row[8].find("(")+1:row[8].find(")")].replace('<br>', '').replace('</br>', '')
					spell['description'] = row[8].replace(row[8][row[8].find("("):row[8].find(")")+1], '').replace('<br>', '').replace('</br>', '')
				else:
					spell['material'] = 0
					spell['ingredients'] = 'None'
					spell['description'] = row[8].replace('<br>', '').replace('</br>', '')

				spell['casting_time'] = row[4]
				spell['range'] = row[5]
				spell['duration'] = row[7]


				spells.append(spell)


#SQLAlchamy Part
#Declare success variables
si = 0
sni = 0
sclc = 0

for spell in spells:
	#Create database session
	session = Session()
	#Add Classes to database if not existing yet
	if session.query(Class).filter(Class.name == spell['class']).first() is None:
		clas = Class()
		clas.name = spell['class']
		session.add(clas)
		session.commit

	#Check if spell already in database and insert if not
	if session.query(Spell).filter(Spell.name == spell['name']).first() is None:
		spelll = Spell()
		spelll.name = spell['name']
		spelll.level = spell['level']
		spelll.school = spell['school']
		spelll.verbal = spell['verbal']
		spelll.somatic = spell['somatic']
		spelll.material = spell['material']
		spelll.ingredients = spell['ingredients']
		spelll.casting_time = spell['casting_time']
		spelll.range = spell['range']
		spelll.duration = spell['duration']
		spelll.description = spell['description']
		session.add(spelll)
		session.commit()
		si += 1
	else:
		sni += 1

	#Query database
	classid = session.query(Class.id).filter(Class.name == spell['class']).first()
	spellid = session.query(Spell.id).filter(Spell.name == spell['name']).first()

	#Link Spell and Class in the 'CSL' ClassSpellLinking table
	if session.query(CSL.spell_id, CSL.class_id).filter(CSL.class_id == classid.id, CSL.spell_id == spellid.id).first() is None:
		csll = CSL()
		csll.class_id = classid.id
		csll.spell_id = spellid.id
		session.add(csll)
		session.commit()
		sclc += 1
	
	#End Database session
	session.close()


#Tell the user the results
print("DONE! %s Spells inserted! %s already in the database! %s Links created!" % (si, sni, sclc))