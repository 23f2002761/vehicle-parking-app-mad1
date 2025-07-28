from flask import Blueprint, render_template, session, redirect, url_for

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/admin/dashboard')
def admin():
    if session.get('is_admin'):
        return render_template('admin_dashboard.html')   
    return redirect(url_for('authentication.login'))

@dashboard_bp.route('/user/dashboard')
def user():
    if session.get('is_admin'):
        return redirect(url_for('dashboard.admin'))
    return render_template('user_dashboard.html',username=session.get('username'))
