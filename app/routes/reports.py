from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from app.models import Report

bp = Blueprint('reports', __name__, template_folder='../templates')

@bp.route('/')
def list_reports():
    reports = Report.query.order_by(Report.timestamp.desc()).all()
    return render_template('reports_list.html', reports=reports)

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_report():
    if request.method == 'POST':
        rpt = Report(
            title=request.form['title'],
            description=request.form['description'],
            location=request.form.get('location'),
            latitude=request.form.get('latitude'),
            longitude=request.form.get('longitude'),
            created_by=current_user.id
        )
        db.session.add(rpt)
        db.session.commit()
        flash('Report submitted!', 'success')
        return redirect(url_for('reports.show_report', report_id=rpt.id))
    return render_template('report_form.html')

@bp.route('/<int:report_id>')
def show_report(report_id):
    rpt = Report.query.get_or_404(report_id)
    return render_template('report_detail.html', rpt=rpt)
