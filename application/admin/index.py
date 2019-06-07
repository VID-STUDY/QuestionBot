from . import bp
from flask import send_file, current_app, url_for
from flask_login import login_required
import os


@bp.route('/', defaults={'path': ''})
@bp.route('/<path:path>')
@login_required
def index_client(path):
    dist_dir = current_app.config['DIST_DIR']
    entry = os.path.join(dist_dir, 'index.html')
    return send_file(entry)
