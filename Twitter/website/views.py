from flask import Blueprint, render_template, request
from flask import flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Tweets, Library
from . import db
import json

views = Blueprint('views', __name__)

def DeleteLib(lib):
    todel = db.session.query(Library).filter_by(name = lib, user_id = current_user.id)
    lib_id = todel.first().__dict__['id']
    todel2 = db.session.query(Note).filter_by(lib_id = lib_id)
    todel.delete(synchronize_session=False)
    todel2.delete(synchronize_session=False)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    dest = "home.html"
    if request.method == 'POST':
        req_cat = request.form.get('category')
        if req_cat:
            req_cat = req_cat.replace(" ", "_")
            lib_query = Library.query.filter_by(name = req_cat, user_id = current_user.id).all()
            if len(lib_query) == 0:
                new_lib = Library(user_id=current_user.id, name=req_cat)
                db.session.add(new_lib)
                db.session.commit()
            else:
                flash('This category already exists!', category='error')
            dest = "home.html"
        elif request.form.get('del'):
            dest = "home.html"
        elif request.form.getlist('delete'):
            delete = request.form.getlist('delete')
            [DeleteLib(i) for i in delete if i != ""]
            db.session.commit()
            dest = "home.html"
        else:
            req_select = request.form.get('select')
            if req_select:
                dest = str(req_select)+".html"
                return redirect(url_for('views.note', name = req_select))

    return render_template(dest, user=current_user)