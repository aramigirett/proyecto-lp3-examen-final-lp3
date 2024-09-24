from flask import Blueprint, render_template

telmod = Blueprint('telefono', __name__, template_folder='templates')

@telmod.route('/telefono-index')
def telefonoIndex():
    return render_template('telefono-index.html')