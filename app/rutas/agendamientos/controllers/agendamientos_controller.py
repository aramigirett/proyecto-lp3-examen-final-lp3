# agendamientos/controllers/agendamientos_controller.py
from agendamientos.models.paciente import Paciente

def registrar_paciente(data):
    paciente = Paciente(data['nombre'], data['edad'])
    paciente_id = paciente.guardar()
    Paciente.registrar_cita(paciente_id, data['fecha'], data['hora'])

def mostrar_calendario():
    citas = Paciente.obtener_citas()
    return citas