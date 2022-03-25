from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from .models import PEP, Log
from . import db
from flask import flash
from os import path
import json
import csv
DB_NAME = 'database.db'


views = Blueprint('views', __name__)

@views.route('/', methods = ['GET', 'POST'])
@login_required
def home():

    if not PEP.query.filter_by(name='name').first():
        file = open('PEP-Check/website/pep.csv')
        data = csv.reader(file)

        print('Inne')
        test = 0
        for i in data:
            if test < 3:
                print(f'Data nummer 1: {i}')
            test += 1

            person = PEP(name = i[2].lower())
            db.session.add(person)
            db.session.commit()
        dataimported = False
        


    if(request.method == 'POST'):
        pep = request.form.get('pep')

        temp = path.exists('PEP-Check/website/database.db')
        print(f'Does db exist?: {temp}')
        print(pep)

        if(pep):
            print('data: ', pep)
            if(len(pep)<1):
                flash('Name is too short', category='error')
            
            else:
                pep = pep.lower().strip()
                found_pep = PEP.query.filter_by(name=pep).first()
                if(found_pep):
                    flash('This person is a politically exposed person!', category='error')
                    print(found_pep)
                    new_search = Log(name=pep, user_id=current_user.id)
                    db.session.add(new_search)
                    db.session.commit()
                else:
                    flash('This person is NOT a politically exposed person!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delte-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Log.query.get(noteId)
    if(note):
        if(note.user_id==current_user.id):
            db.session.delete(note)
            db.session.commit()
            return jsonify({})
