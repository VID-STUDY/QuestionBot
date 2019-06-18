from . import bp
from .forms import NewQuizForm
from application.core.services import quizzes
from flask import render_template, url_for, redirect, flash, abort
from flask_login import login_required
from application.core.models import Channel, Quiz


@bp.route('/channels/<int:channel_id>/quizzes', methods=['GET'])
@login_required
def channel_quizzes(channel_id):
    chann_quizzes = Channel.get_quizzes_by_channel_id(channel_id)
    if channel_quizzes is None:
        abort(404)
    return render_template('admin/quizzes.html', quizzes=chann_quizzes)


@bp.route('/channels/<int:channel_id>/quizzes/create', methods=['GET', 'POST'])
@login_required
def create_quiz(channel_id: int):
    form = NewQuizForm()
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        top_count = int(form.top_count.data)
        quizzes.create_quiz(start_date, end_date, top_count, channel_id)
        flash('Викторина {} - {} создана!'.format(start_date, end_date), category='success')
        return redirect(url_for('admin.channel_quizzes'))
    return render_template('admin/new-quiz.html', form=form)


@bp.route('/channels/<int:channel_id>/quizzes/<int:quiz_id>', methods=['GET'])
@login_required
def show_quiz(quiz_id: int, channel_id: int):
    quiz = Quiz.get_by_id(quiz_id)
    return render_template('admin/quiz.html', quiz=quiz, channel_id=channel_id)


@bp.route('/channels/<int:channel_id>/<int:quiz_id>/remove', methods=['GET'])
@login_required
def remove_quiz(quiz_id: int, channel_id: int):
    # TODO: Delete all scheduled jobs and files with tests in this quiz
    Quiz.remove(quiz_id)
    return redirect(url_for('admin.channel_quizzes', channel_id=channel_id))
