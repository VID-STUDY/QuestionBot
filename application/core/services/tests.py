from application import db
from application.core.models import Test, Option, Quiz
from datetime import datetime
from config import Config
from werkzeug.utils import secure_filename
from application.utils import files
import os


def create_test(question: str, publish_date: str, publish_time: str,
                quiz_id: int, options: list, file):
    publish_date_time = datetime.strptime(publish_date + ' ' + publish_time, '%d.%m.%Y %H:%M')
    quiz = Quiz.get_by_id(quiz_id)
    channel_id = quiz.channel_id
    test = Test(question=question, quiz_id=quiz_id, channel_id=channel_id, publish_date=publish_date_time)
    for option in options:
        option = Option(value=option.value, is_answer=option.is_answer)
        test.options.append(option)
        db.session.add(option)
    if file and file.filename != '':
        file_path = os.path.join(Config.UPLOAD_FOLDER, secure_filename(file.filename))
        files.save_file(file, file_path, recreate=True)
        test.file_path = file_path
    db.session.add(test)
    db.session.commit()
    return test


def update_test(test_id: int, question: str, publish_date: str, publish_time: str,
                options: list = None, file=None):
    test = Test.query.get_or_404(test_id)
    test.question = question
    publish_date_time = datetime.strptime(publish_date + ' ' + publish_time, '%d.%m.%Y %H:%M')
    test.publish_date = publish_date_time
    if options:
        current_options = test.options.all()
        for option in current_options:
            db.session.delete(option)
        for option in options:
            option = Option(value=option.value, is_answer=option.is_answer)
            test.options.append(option)
            db.session.add(option)
    if file and file.filename != '':
        if test.file_path:
            files.remove_file(test.file_path)
        file_path = os.path.join(Config.UPLOAD_FOLDER, secure_filename(file.filename))
        files.save_file(file, file_path, recreate=True)
        test.file_path = file_path
    db.session.commit()
    return test


def remove_test(test_id):
    test = Test.query.get_or_404(test_id)
    if test.file_path:
        files.remove_file(test.file_path)
    db.session.delete(test)
    db.session.commit()


def get_tests_by_quiz_id(quiz_id: int):
    quiz = Quiz.query.get_or_404(quiz_id)
    return quiz.tests.order_by(Test.publish_date.desc()).all()


def get_by_id(test_id):
    return Test.query.get_or_404(test_id)
