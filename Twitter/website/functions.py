from flask_login import current_user
from .models import Friend, User
from os import path

def getFriends():
    friends = []
    sender_is_friend = Friend.query.filter_by(follower_user_id = current_user.id).all()
    sender_list = []
    for i in sender_is_friend:
        sender_list.append(i.__dict__['followed_user_id'])
    for i in sender_list:
        q = Friend.query.filter_by(follower_user_id = i).all()
        q_list = [j.__dict__['followed_user_id'] for j in q]
        if current_user.id in q_list:
            qu = User.query.filter_by(id = i).first().__dict__
            if not path.exists('website/static/images/' + qu['username'] + ".png"):
                x = [qu['first_name'] + ' ' + qu['last_name'], "base", qu['id']]
            else:
                x = [qu['first_name'] + ' ' + qu['last_name'], qu['username'], qu['id']]
            friends.append(x)

    return friends


def getMessages(rec_user, usr_id):
    l = []
    for i in current_user.message:
        if i.reciever_id == int(usr_id):
            l.append([i.data, i.date, i.sender_id])
    for i in rec_user:
        if i.__dict__['reciever_id'] == current_user.id:
            l.append([i.__dict__['data'], i.__dict__['date'], i.__dict__['sender_id']])
    l.sort(key=lambda x: x[1])
    return l

def getFriendsID():
    friends = []
    sender_is_friend = Friend.query.filter_by(follower_user_id = current_user.id).all()
    sender_list = []
    for i in sender_is_friend:
        sender_list.append(i.__dict__['followed_user_id'])
    for i in sender_list:
        q = Friend.query.filter_by(follower_user_id = i).all()
        q_list = [j.__dict__['followed_user_id'] for j in q]
        if current_user.id in q_list:
            qu = User.query.filter_by(id = i).first().__dict__
            x = qu['id']
            friends.append(x)

    return friends