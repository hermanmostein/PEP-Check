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

    if(request.method == 'GET'):
        if not path.exists('PEP-Check/website/database.db'):

            file = open('PEP-Check/website/pep.csv')
            data = csv.reader(file)

            for i in data:
                person = PEP(name = i[2])
                db.session.add(person)
            db.session.commit()


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
                if(PEP.query.filter_by(name=pep)):
                    flash('This person is a politically exposed person!', category='error')
                    new_search = Log(name=pep, user_id=current_user.id)
                    db.session.add(new_search)
                    db.session.commit()
                    #flash('Note added!', category='success')
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
