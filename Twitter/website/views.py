from flask import Blueprint, render_template, request
from flask import flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Message, User, Friend
from . import db
from .functions import getFriends, getMessages, getFriendsID, getRequests
from os import path

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    q = Message.query.filter_by(sender_id = current_user.id).all()
    if len(q) == 0:
        dest = "home.html"
    else:
        last = Message.query.filter_by(sender_id = current_user.id).first()
        return redirect(url_for('views.messenger', usr_id = last.__dict__['reciever_id'] ))
    

    if request.method == 'POST':
        usr = request.form.get('user')
        if usr:
            usr = int(usr)
            return redirect(url_for('views.messenger', usr_id = usr ))

    friends = getFriends()[0]

    if not path.exists('website/static/images/' + current_user.username + ".png"):
        userpicture = "base"
        return render_template(dest, user=current_user, pic=userpicture, friends=friends)
    else:
        userpicture = current_user.username
        return render_template(dest, user=current_user, pic=userpicture, friends=friends)

@views.route('/t/<usr_id>', methods=['GET', 'POST'])
def messenger(usr_id):

    friendID = getFriendsID()
    if int(usr_id) not in friendID:
        return render_template('404.html')

    num = User.query.count()

    """if request.method == 'GET':"""
        

    if int(usr_id) != current_user.id and int(usr_id) <= num:
        if request.method == 'POST':
            message = request.form.get('message')
            usr = request.form.get('user')
            if message:
                new_message = Message(data = message, sender_id = current_user.id, reciever_id =  usr_id)
                db.session.add(new_message)
                db.session.commit()
                return redirect(url_for('views.messenger', usr_id = usr_id ))
            elif usr:
                usr = int(usr)
                return redirect(url_for('views.messenger', usr_id = usr ))

        qu = User.query.filter_by(id=usr_id).first().__dict__

        rec_Name = qu['first_name'].capitalize() + " " + qu['last_name'].capitalize()
        rec_name = qu['username'] if path.exists('website/static/images/' + qu['username'] + ".png") else "base"
        rec_user = db.session.query(Message).filter_by(sender_id=usr_id).all()

        messages = getMessages(rec_user, usr_id)

        friends = getFriends()[0]

        if not path.exists('website/static/images/' + current_user.username + ".png"):
            userpicture = "base"
            return render_template('messenger.html', friends=friends, user=current_user, pic=userpicture, sender=current_user.id, reciever=int(usr_id), rec_name=rec_name, rec_Names=rec_Name, messages=messages)
        else:
            userpicture = current_user.username
            return render_template('messenger.html', friends=friends, user=current_user, pic=userpicture, sender=current_user.id, recstr=usr_id, reciever=int(usr_id), rec_name=rec_name, rec_Names=rec_Name, messages=messages)
    else:
        return render_template('404.html')


@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', category='error')
            return render_template("profile.html", user=current_user)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', category='error')
            return render_template("profile.html", user=current_user)
        if file:
            filename = f"{current_user.username}.png"
            file.save(f"website/static/images/{filename}")

    if not path.exists('website/static/images/' + current_user.username + ".png"):
        userpicture = "base"
        return render_template("profile.html", pic=userpicture, user=current_user)
    else:
        userpicture = current_user.username
        return render_template("profile.html", pic=userpicture, user=current_user)

@views.route('/addFriend', methods=['GET', 'POST'])
@login_required
def addFriend():

    names = getFriends()[1]

    if not path.exists('website/static/images/' + current_user.username + ".png"):
        userpicture = "base"
    else:
        userpicture = current_user.username

    if request.method == 'POST':
        search_string = request.form.get('search')
        usr = request.form.get('user')
        re = request.form.get('re')
        re_decline = request.form.get('re_decline')
        if search_string:
            result = db.session.query(User).filter(User.name.contains(search_string)).all()
            result1 = []
            for i in result:
                uname = i.__dict__['username']
                if uname not in names and uname != current_user.username:
                    if not path.exists('website/static/images/' + uname + ".png"):
                        pname = "base"
                    else:
                        pname = uname
                    result1.append([i.__dict__['name'], pname, i.__dict__['id']])
            redirect(url_for('views.addFriend'))
        elif usr:
            new_request = Friend(follower_user_id = current_user.id, followed_user_id = int(usr))
            db.session.add(new_request)
            db.session.commit()
            result1 = []
        elif re:
            new_request = Friend(follower_user_id = current_user.id, followed_user_id = int(re))
            db.session.add(new_request)
            db.session.commit()
            result1 = []
            redirect(url_for('views.addFriend'))
        elif re_decline:
            Friend.query.filter_by(id=int(re_decline)).delete()
            db.session.commit()
            result1 = []
        else:
            result = []
    else:
            result1 = []

    req = getRequests()

    friends = getFriends()[0]

    return render_template("addfriend.html", pic=userpicture, user=current_user, req=req, result=result1, friends=friends)