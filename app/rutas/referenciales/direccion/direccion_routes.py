from flask import Blueprint, render_template

diremod = Blueprint('direccion', __name__, template_folder='templates')

@diremod.route('/direccion-index')
def direccionIndex():
    return render_template('direccion-index.html')