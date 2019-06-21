from . import bp
from .forms import TestForm
from flask import render_template, url_for, redirect, flash
from flask_login import login_required

from application.core.services import tests, quizzes
from application.core.models import Answer
from application.core import schedule


@bp.route('/quizzes/<int:quiz_id>/tests')
@login_required
def quizzes_tests(quiz_id: int):
    quiz_polls = tests.get_tests_by_quiz_id(quiz_id)
    quiz = quizzes.get_by_id(quiz_id)
    return render_template('admin/tests-list.html', tests=quiz_polls, quiz=quiz)


@bp.route('/quizzes/<int:quiz_id>/tests/<int:test_id>', methods=['GET', 'POST'])
@login_required
def show_test(test_id: int, quiz_id: int):
    form = TestForm()
    if form.validate_on_submit():
        question = form.question.data
        date = form.publish_date.data
        time = form.publish_time.data
        file = form.file.data
        options = form.options.entries
        test = tests.update_test(test_id, question, date, time, options, file)
        schedule.update_test_date_publish(test.id, test.publish_date)
        flash('Тест {} изменён!'.format(question), category='success')
        return redirect(url_for('admin.quizzes_tests', quiz_id=quiz_id))
    test = tests.get_by_id(test_id)
    quiz = quizzes.get_by_id(quiz_id)
    answers = test.answers.filter(Answer.is_right == True, Answer.points != 0).order_by(Answer.created_at.desc()).all()
    form.fill_from_object(test)
    return render_template('admin/test.html', form=form, test=test, quiz=quiz, answers=answers)


@bp.route('/quizzes/<int:quiz_id>/tests/new', methods=['GET', 'POST'])
@login_required
def create_test(quiz_id: int):
    form = TestForm()
    if form.validate_on_submit():
        question = form.question.data
        publish_date = form.publish_date.data
        publish_time = form.publish_time.data
        file = form.file.data
        options = form.options.entries
        test = tests.create_test(question, publish_date, publish_time, quiz_id, options, file)
        schedule.add_test_to_publish(test.id, test.publish_date)
        flash("Тест {} добавлен".format(question), category='success')
        return redirect(url_for('admin.quizzes_tests', quiz_id=quiz_id))
    quiz = quizzes.get_by_id(quiz_id)
    form.init()
    form.set_start_end_dates(quiz.start_date, quiz.end_date)
    return render_template('admin/new-test.html', form=form, quiz=quiz)


@bp.route('/quizzes/<int:quiz_id>/tests/<int:test_id>/remove')
@login_required
def remove_test(test_id: int, quiz_id: int):
    tests.remove_test(test_id)
    schedule.remove_test_from_publishing(test_id)
    return redirect(url_for('admin.quizzes_tests', quiz_id=quiz_id))
