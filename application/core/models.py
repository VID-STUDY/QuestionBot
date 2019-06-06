from application import db
from datetime import datetime
import settings
from application.utils import date as dateutils
from sqlalchemy import func
from werkzeug.utils import secure_filename
from application.utils import files
from config import Config
import os

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
    chat_id = db.Column(db.BigInteger)
    channel_name = db.Column(db.String(100))
    channel_title = db.Column(db.String(100))
    members = db.relationship('BotUser', secondary=members, lazy='dynamic', backref=db.backref('channels', lazy=True))
    quizzes = db.relationship('Quiz', lazy='dynamic', backref='channel')

    def to_dict(self):
        return {
            'id': self.id,
            'chatId': self.chat_id,
            'channelName': self.channel_name,
            'channelTitle': self.channel_title
        }

    @staticmethod
    def add(channel_name, channel_title, chat_id):
        channel = Channel(channel_name=channel_name, channel_title=channel_title, chat_id=chat_id)
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
    
    @staticmethod
    def get_quizzes_by_channel_name(channel_name: str):
        channel = Channel.get_by_name(channel_name)
        if not channel:
            return None
        return channel.quizzes.order_by(Quiz.id.desc()).all()

    def is_member_exists(self, bot_user_id: int) -> bool:
        return self.members.filter(members.c.bot_user_id == bot_user_id).count() > 0

    def add_member(self, bot_user: BotUser):
        if not self.is_member_exists(bot_user.id):
            self.members.append(bot_user)

    def remove_member(self, bot_user: BotUser):
        if self.is_member_exists(bot_user.id):
            self.members.remove(bot_user)

    def get_current_quiz(self):
        now = datetime.utcnow()
        return self.quizzes.filter(Quiz.start_date <= now <= Quiz.end_date).first()


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
    publish_date = db.Column(db.DateTime)
    file_path = db.Column(db.String(150))
    published = db.Column(db.Boolean, default=False)
    options = db.relationship('Option', lazy='dynamic', cascade="all,delete-orphan")
    answers = db.relationship('Answer', lazy='dynamic', cascade="all,delete-orphan")

    def to_dict(self):
        options = self.options.all()
        if self.file_path:
            file = os.path.basename(self.file_path)
        else:
            file = None
        return {
            'id': self.id,
            'question': self.question,
            'quizId': self.quiz_id,
            'publishDate': self.publish_date.strftime('%d.%m.%Y %H:%M'),
            'file': file,
            'options': [option.to_dict() for option in options],
            'answersCount': self.answers.count()
        }

    @staticmethod
    def create(json):
        test = Test()
        test.question = json['question']
        date_json = json['publishDate']
        time_json = json['publishTime']
        test.publish_date = dateutils.convert_asia_tz_to_utc(datetime.strptime(date_json + ' ' + time_json,
                                                                               '%d.%m.%Y %H:%M'))
        new_options = Option.from_jsons(json['options'])
        for opt in new_options:
            test.options.append(opt)
            db.session.add(opt)
        test.quiz_id = json['quizId']
        db.session.add(test)
        db.session.commit()
        return test

    @staticmethod
    def get_by_id(test_id: int):
        return Test.query.get(test_id)
    
    @staticmethod
    def save_file(test_id: int, file):
        test = Test.get_by_id(test_id)
        if test.file_path:
            files.remove_file(test.file_path)
        file_path = os.path.join(Config.UPLOAD_FOLDER, secure_filename(file.filename))
        files.save_file(file, file_path, recreate=True)
        test.file_path = file_path
        db.session.commit()
    
    @staticmethod
    def update(test_id: int, json: dict):
        test = Test.get_by_id(test_id)
        test.question = json['question']
        test.publish_date = dateutils.convert_asia_tz_to_utc(datetime.strptime(json['publishDate'], '%d.%m.%Y'))
        new_options = Option.from_jsons(json['options'])
        current_options = test.options.all()
        for option in current_options:
            db.session.delete(option)
        for opt in new_options:
            test.options.append(opt)
            db.session.add(opt)
        db.session.commit()
        return test
    
    @staticmethod
    def remove(test_id: int):
        db.session.delete(Test.get_by_id(test_id))
        db.session.commit()

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

    def make_published(self):
        self.published = True
        db.session.commit()


class Quiz(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    top_count = db.Column(db.Integer)
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'))
    tests = db.relationship('Test', lazy='dynamic', backref='quiz', cascade='all,delete-orphan')

    def to_dict(self):
        tests = self.tests.all()
        return {
            'id': self.id,
            'startDate': self.start_date.strftime('%d.%m.%Y'),
            'endDate': self.end_date.strftime('%d.%m.%Y'),
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
    
    @staticmethod
    def update(quiz_id: int, json: dict):
        quiz = Quiz.get_by_id(quiz_id)
        quiz.startDate = dateutils.convert_asia_tz_to_utc(datetime.strptime(json['startDate'], '%d.%m.%Y'))
        quiz.end_date = dateutils.convert_asia_tz_to_utc(datetime.strptime(json['endDate'], '%d.%m.%Y'))
        quiz.top_count = json['topCount']
        db.session.commit()
        return quiz
    
    @staticmethod
    def remove(quiz_id: int):
        db.session.delete(Quiz.query.get(quiz_id))
        db.session.commit()
    
    @staticmethod
    def get_by_id(quiz_id: int):
        return Quiz.query.get(quiz_id)
    
    @staticmethod
    def get_tests_by_quiz_id(quiz_id: int):
        quiz = Quiz.get_by_id(quiz_id)
        if not quiz:
            return None
        return quiz.tests.all()

    def get_published_tests(self):
        return self.tests.filter(Test.published == True).all()


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('bot_user.id'))
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'))
    points = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    channel_id = db.Column(db.Integer)

    @staticmethod
    def get_summary_user_points_by_channel_and_period(channel_id: int, start_date: datetime, end_date: datetime):
        # TODO: Переписать запрос. Фильтровать от большего к меньшему. Установить лимит
        points_by_users = db.query(BotUser.first_name, func.sum(Answer.points))\
            .filter(Answer.channel_id == channel_id and (start_date <= Answer.created_at <= end_date))\
            .group_by(BotUser.first_name).all()
        return points_by_users


class Poll:
    def __init__(self, question: str, options: list):
        self.question = question
        self.options = options
