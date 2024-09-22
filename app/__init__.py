from flask import Flask

app = Flask(__name__)

# importar referenciales
from app.rutas.referenciales.ciudad.ciudad_routes import ciumod
from app.rutas.referenciales.paises.pais_routes import paimod
from app.rutas.referenciales.correo.correo_routes import cormod


# registrar referenciales
modulo0 = '/referenciales'
app.register_blueprint(ciumod, url_prefix=f'{modulo0}/ciudad')
app.register_blueprint(paimod, url_prefix=f'{modulo0}/paises')
app.register_blueprint(cormod, url_prefix=f'{modulo0}/correo')


#ciudad
from app.rutas.referenciales.ciudad.ciudad_api import ciuapi

#pais
from app.rutas.referenciales.paises.pais_api import paisapi

#coreo
from app.rutas.referenciales.correo.correo_api import correoapi

# APIS v1
#Ciudad
version1 = '/api/v1'
app.register_blueprint(ciuapi, url_prefix=version1)

#Pais
version1 = '/api/v1'
app.register_blueprint(paisapi, url_prefix=version1)

#correo
version1 = '/api/v1'
app.register_blueprint(correoapi, url_prefix=version1)