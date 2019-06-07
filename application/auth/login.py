from . import bp
from flask import render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm
from application.core.models import AdminUser


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return '', 200


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = AdminUser.get_by_email(form.email.data)
        login_user(user, remember=False)
        return redirect(url_for('admin.index'))
    return render_template('auth/login.html', title="Вход в систему", form=form)
