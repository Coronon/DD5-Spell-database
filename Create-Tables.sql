/*These commands create the initial tables*/

CREATE TABLE spells(spell_id INTEGER PRIMARY KEY AUTOINCREMENT, spell_name TEXT UNIQUE, level INTEGER, school TEXT, verbal BOOLEAN, somatic BOOLEAN, material BOOLEAN, ingredients TEXT, casting_time TEXT, range TEXT, duration TEXT, spell_description TEXT);

CREATE TABLE classes(class_id INTEGER PRIMARY KEY AUTOINCREMENT, class_name TEXT UNIQUE);

CREATE TABLE classSpellLink(combo_id INTEGER PRIMARY KEY AUTOINCREMENT, spell_id INTEGER, class_id INTEGER);