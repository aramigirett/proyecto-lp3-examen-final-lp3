from flask import Blueprint, render_template

cormod = Blueprint('correo', __name__, template_folder='templates')

@cormod.route('/correo-index')
def correoIndex():
    return render_template('correo-index.html')