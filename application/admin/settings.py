from . import bp
from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from .forms import SettingsForm
import settings as app_settings


@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        right_answer_points = form.right_answer_point.data
        app_settings.set_right_answer_points(right_answer_points)
        flash('Настройки викторин изменены!', category='success')
        return redirect(url_for('admin.settings'))
    form.fill_from_settings()
    bot_state = app_settings.get_bot_state()
    return render_template('admin/settings.html', form=form, bot_state=bot_state)
