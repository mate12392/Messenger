from flask_login import current_user
from .models import Friend, User, Message
from os import path

def getFriends():
    friends = []
    name = []
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
            y = qu['username']
            friends.append(x)
            name.append(y)

    return friends, name


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

def getRequests():
    req = []
    qu = Friend.query.filter_by(followed_user_id = current_user.id).all()
    for i in qu:
        usr_id = int(i.__dict__['follower_user_id'])
        isfriend = Friend.query.filter_by(followed_user_id = usr_id).all()
        isfriend = [j.__dict__['follower_user_id'] for j in isfriend]
        if i.__dict__['followed_user_id'] not in isfriend:
            qu1 = User.query.filter_by(id = usr_id).first().__dict__

            if not path.exists('website/static/images/' + qu1['username'] + ".png"):
                req.append([int(qu1['id']), f"{qu1['first_name']} {qu1['last_name']}", "base", i.__dict__['id']])
            else:
                req.append([int(qu1['id']), f"{qu1['first_name']} {qu1['last_name']}", qu1['username'], i.__dict__['id']])

    return req