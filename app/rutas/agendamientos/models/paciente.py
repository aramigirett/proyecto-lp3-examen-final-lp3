# agendamientos/models/paciente.py

from app.conexion.Conexion import Conexion

class Paciente:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def guardar(self):
        cursor = Conexion.cursor()
        cursor.execute("INSERT INTO pacientes (nombre, edad) VALUES (%s, %s) RETURNING id", (self.nombre, self.edad))
        paciente_id = cursor.fetchone()[0]
        Conexion.commit()
        cursor.close()
        return paciente_id

    @staticmethod
    def registrar_cita(paciente_id, fecha, hora):
        cursor = Conexion.cursor()
        cursor.execute("INSERT INTO citas (paciente_id, fecha, hora) VALUES (%s, %s, %s)", (paciente_id, fecha, hora))
        Conexion.commit()
        cursor.close()

    @staticmethod
    def obtener_citas():
        cursor = Conexion.cursor()
        cursor.execute("""
            SELECT pacientes.nombre, citas.fecha, citas.hora
            FROM citas
            JOIN pacientes ON citas.paciente_id = pacientes.id
        """)
        citas = cursor.fetchall()
        cursor.close()
        return citas