from application import db
from datetime import datetime
from typing import List


members = db.Table('channel_members',
                   db.Column('bot_user_id', db.Integer, db.ForeignKey('bot_user.id'), primary_key=True),
                   db.Column('channel_id', db.Integer, db.ForeignKey('channel.id'), primary_key=True))


class BotUser(db.Model):
    __tablename__ = 'bot_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    answers = db.relationship('Answer', lazy='dynamic', backref=db.backref('user', lazy=True))


class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer)
    channel_name = db.Column(db.String(100))
    channel_title = db.Column(db.String(100))
    members = db.relationship('BotUser', secondary=members, lazy='dynamic', backref=db.backref('channels', lazy=True))
    tests = db.relationship('Test', lazy='dynamic', backref='channel')

    def to_dict(self):
        return {
            'id': self.id,
            'channelName': self.channel_name,
            'channelTitle': self.channel_title
        }

    @staticmethod
    def add(channel_name, channel_title):
        channel = Channel(channel_name=channel_name, channel_title=channel_title)
        db.session.add(channel)
        db.session.commit()
        return channel

    @staticmethod
    def get_tests_by_name(channel_name: str):
        channel = Channel.query.filter(Channel.channel_name == channel_name).first()
        if not channel:
            return None
        return channel.tests.all()

    @staticmethod
    def get_by_name(channel_name: str):
        return Channel.query.filter(Channel.channel_name == channel_name).first()

    def is_member_exists(self, bot_user_id: int) -> bool:
        return self.members.filter(members.c.bot_user_id == bot_user_id).count() > 0

    def add_member(self, bot_user: BotUser):
        if not self.is_member_exists(bot_user.id):
            self.members.append(bot_user)

    def remove_member(self, bot_user: BotUser):
        if self.is_member_exists(bot_user.id):
            self.members.remove(bot_user)


class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(100))
    is_answer = db.Column(db.Boolean, default=False)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'value': self.value,
            'isAnswer': self.is_answer
        }

    @staticmethod
    def from_jsons(json_options):
        return [Option(value=opt['value'], is_answer=opt['isAnswer']) for opt in json_options]


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(150))
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'))
    options = db.relationship('Option', lazy='dynamic')
    answers = db.relationship('Answer', lazy='dynamic')

    def to_dict(self):
        options = self.options.all()
        return {
            'id': self.id,
            'question': self.question,
            'channel_id': self.channel_id,
            'options': [option.to_dict() for option in options]
        }

    @staticmethod
    def create(json, channel: Channel):
        test = Test()
        test.question = json['question']
        new_options = Option.from_jsons(json['options'])
        for opt in new_options:
            test.options.append(opt)
            db.session.add(opt)
        channel.tests.append(test)
        db.session.add(test)
        db.session.commit()
        return test

    def add_answer(self, user_id: int, answer):
        if self.answers.filter(Answer.user_id == user_id).count() == 0:
            self.answers.append(answer)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('bot_user.id'))
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'))
    points = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Poll:
    def __init__(self, question: str, options: list):
        self.question = question
        self.options = options
