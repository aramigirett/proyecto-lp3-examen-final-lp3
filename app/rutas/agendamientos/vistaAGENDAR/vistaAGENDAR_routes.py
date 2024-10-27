from flask import Blueprint, render_template, request, redirect, url_for
from app.rutas.agendamientos.vistaAGENDAR.vistaAGENDAR_routes import registrar_paciente, mostrar_calendario

vistagendamod = Blueprint('vistaAGENDAR', __name__, template_folder='templates')

# Ruta para mostrar el calendario con citas
@vistagendamod.route('/agendamientos')
def calendario():
    citas = mostrar_calendario()
    return render_template("vistagendar/vistagendar-index.html", citas=citas)

# Ruta para mostrar el formulario de registro de paciente
@vistagendamod.route('/agendamientos/registrar_paciente', methods=['GET'])
def formulario_paciente():
    return render_template("vistagendar/registrar_paciente.html")

# Ruta para procesar los datos del formulario de paciente
@vistagendamod.route('/agendamientos/registrar_paciente', methods=['POST'])
def registrar_paciente_route():
    data = request.form.to_dict()
    registrar_paciente(data)
    return redirect(url_for('vistaAGENDAR.calendario'))