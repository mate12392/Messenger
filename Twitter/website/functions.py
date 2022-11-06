from flask_login import current_user
from .models import Friend

def getFriends(recipient_id):
    sender_is_friend = Friend.query.filter_by(follower_user_id = current_user.id).all()
    sender_list = []
    for i in sender_is_friend:
        sender_list.append(i.__dict__['followed_user_id'])
    recipient_is_friend = Friend.query.filter_by(followed_user_id = recipient_id).all()
    recipient_list = []
    for i in recipient_is_friend:
        recipient_list.append(i.__dict__['followed_user_id'])
    if recipient_id in sender_list and current_user.id in recipient_list:
        return True
    else:
        return False

def getMessages(rec_user):
    l = []
    for i in current_user.message:
        l.append([i.data, i.date, i.sender_id])
    for i in rec_user:
        l.append([i.__dict__['data'], i.__dict__['date'], i.__dict__['sender_id']])
    l.sort(key=lambda x: x[1])
    return l