from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from app.models import Report, User

bp = Blueprint('admin', __name__, template_folder='../templates')

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.role != 'admin':
            flash('Admin access only.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated

@bp.route('/')
@login_required
@admin_required
def dashboard():
    reports = Report.query.order_by(Report.timestamp.desc()).all()
    volunteers = User.query.filter_by(role='volunteer').all()
    return render_template('admin_dashboard.html',
                           reports=reports,
                           volunteers=volunteers)

@bp.route('/assign/<int:report_id>', methods=['POST'])
@login_required
@admin_required
def assign(report_id):
    rpt = Report.query.get_or_404(report_id)
    rpt.assigned_to = int(request.form['volunteer_id'])
    rpt.status = 'in_progress'
    db.session.commit()
    flash('Assigned!', 'success')
    return redirect(url_for('admin.dashboard'))

@bp.route('/status/<int:report_id>', methods=['POST'])
@login_required
@admin_required
def change_status(report_id):
    rpt = Report.query.get_or_404(report_id)
    rpt.status = request.form['status']
    db.session.commit()
    flash('Status updated.', 'success')
    return redirect(url_for('admin.dashboard'))
