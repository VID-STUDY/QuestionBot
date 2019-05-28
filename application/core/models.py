from application import db
from datetime import datetime
import settings

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

    @staticmethod
    def add_user(user_id, first_name, last_name, username):
        current_user = BotUser.query.get(user_id)
        if current_user:
            return current_user
        new_user = BotUser(id=user_id, username=username, first_name=first_name, last_name=last_name)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def get_name(self):
        if self.last_name:
            return self.first_name + ' ' + self.last_name
        else:
            return self.first_name


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

    @staticmethod
    def get_by_chat_id(channel_chat_id: int):
        return Channel.query.filter(Channel.chat_id == channel_chat_id)

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

    @staticmethod
    def get_by_id(test_id: int):
        return Test.query.get(test_id)

    def add_answer(self, answer):
        self.answers.append(answer)
        db.session.add(answer)
        db.session.commit()

    def get_count_user_answers(self, user_id):
        return self.answers.filter(Answer.user_id == user_id).count()

    def get_right_answer(self) -> Option:
        return self.options.filter(Option.is_answer == True).first()

    def get_count_of_first_try_answers(self):
        top_10_points = settings.get_top_10_points()
        first_try_points = settings.get_first_try_points()
        return self.answers.query(Answer.points == top_10_points or Answer.points == first_try_points).count()

    def get_top_10_answers_count(self):
        top_10_points = settings.get_top_10_points()
        return self.answers.query(Answer.points == top_10_points).count()

    def user_given_right_answer(self, user_id):
        top_10_points = settings.get_top_10_points()
        first_try_points = settings.get_first_try_points()
        return self.answers.query.filter(Answer.user_id == user_id
                                         and (Answer.points == top_10_points
                                              or Answer.points == first_try_points)).count() > 0


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
