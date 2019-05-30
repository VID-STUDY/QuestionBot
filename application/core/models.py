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
    quizzes = db.relationship('Quiz', lazy='dynamic', backref='channel')

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
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))
    options = db.relationship('Option', lazy='dynamic')
    answers = db.relationship('Answer', lazy='dynamic')

    def to_dict(self):
        options = self.options.all()
        return {
            'id': self.id,
            'question': self.question,
            'options': [option.to_dict() for option in options]
        }

    @staticmethod
    def create(json, quiz):
        test = Test()
        test.question = json['question']
        new_options = Option.from_jsons(json['options'])
        for opt in new_options:
            test.options.append(opt)
            db.session.add(opt)
        quiz.tests.append(test)
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

    def user_given_right_answer(self, user_id):
        right_answer_points = settings.get_right_answer_points()
        return self.answers.query.filter(Answer.user_id == user_id and Answer.points == right_answer_points).count() > 0


class Quiz(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    top_count = db.Column(db.Integer)
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'))
    tests = db.relationship('Test', lazy='dynamic', backref='quiz')

    def to_dict(self):
        tests = self.tests.all()
        return {
            'id': self.id,
            'startDate': self.start_date,
            'endDate': self.end_date,
            'topCount': self.top_count,
            'channelId': self.channel_id,
            'tests': [t.to_dict() for t in tests]
        }

    @staticmethod
    def create(json: dict, channel: Channel):
        new_quiz = Quiz()
        new_quiz.start_date = datetime.strptime(json['startDate'], '%d.%m.%Y')
        new_quiz.end_date = datetime.strptime(json['endDate'], '%d.%m.%Y')
        new_quiz.top_count = json['topCount']
        channel.quizzes.append(new_quiz)
        db.session.add(new_quiz)
        db.session.commit()
        return new_quiz


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
