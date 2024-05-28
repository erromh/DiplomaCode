from flask import Blueprint, render_template, request
from flask_login import login_required

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
@login_required
def index():
    return render_template('main/index.html')



@main.route('/mode_selection', methods=['POST'])
def mode_selection():
    selected_option = request.form.get('option')
    return render_template('main/result.html', selected_option=selected_option)

        