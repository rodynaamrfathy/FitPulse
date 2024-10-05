from flask import Blueprint, render_template

dietplans_bp = Blueprint('dietplans', __name__)

@dietplans_bp.route('/dietplans')
def dietplans():
    return render_template('dietplans.html')

@dietplans_bp.route('/dietplan')
def dietplan():
    return render_template('dietplan.html')

