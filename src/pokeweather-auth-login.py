from flask import Flask, jsonify, request, render_template, redirect, url_for, make_response
import requests
import random
import openmeteo_requests
import requests_cache
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import string
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
import time

def generar_contrasena():
    largo = 20
    caracteres = string.ascii_letters + string.digits + string.punctuation
    contrasena = ''.join(random.choice(caracteres) for _ in range(largo))
    return contrasena

app = Flask(__name__)
csrf = CSRFProtect()
app.config['SECRET_KEY'] = generar_contrasena()
login_manager = LoginManager(app)



# Configuracion de sesion de cache y reintento en caso de error para la API de Open-Meteo
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
openmeteo = openmeteo_requests.Client(session=cache_session)

# Configurar conexion con base de datos > por ahora simulada
users = {
    "admin": "admin123",
    "user": "user123"
}

### ----- APIS consulta de clima ----- ###

# API publica para obtenet las coordenadas mediante ubicacion aproximada por IP
def obtener_coordenadas():
    url = 'https://ipinfo.io/json'
    respuesta = requests.get(url)
    datos = respuesta.json()
    coordenadas = datos['loc'].split(',')
    return coordenadas

# Obtencion de la temperatura actual
def obtener_temperatura_actual(latitude, longitude):
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m"
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    return round(current_temperature_2m)


### ----- Clase de usuario ----- ###

class User(UserMixin):
    def __init__(self, username):
        self.username = username

    def get_id(self):
        return self.username

### ----- Carga de Usuario ----- ###

@login_manager.user_loader
def load_user(username):
    if username in users:
        return User(username)
    return None


### ----- Funcion que determina el tipo mas fuerte segun clima ----- ###

# Funcion para determinar el tipo de Pokemon mas fuerte basado en la temperatura
def get_tipo_mas_fuerte_segun_clima(temperatura):

    # Agregue el resto de las clases en el else, limitando ICE hasta -10 Grados
    if temperatura >= 30:
        return 'fire'
    elif temperatura >= 20:
        return 'ground'
    elif temperatura >= 10:
        return 'normal'
    elif temperatura >= 0:
        return 'water'
    elif temperatura >= -10:
        return 'ice'
    else:
        types = ['unknown','dragon','shadow','dark','rock','grass','psychic','flying','bug','fighting''steel','ghost','electric''poison','fairy']
        clase = random.choice(types)
        return clase


# Redireccionamiento directamente a Login
@app.route('/')
def index():
    return redirect(url_for('login'))

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return redirect(url_for('login'))

def status_405(error):
    return redirect(url_for('login'))

# Validacion de user y password
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users or users[username] != password:
            return render_template('login_fail.html')
        
        user = User(username)
        login_user(user)
        return redirect(url_for('home'))

    else:
        return render_template('login.html')


@app.route('/home')
@login_required
def home():
    return render_template('home.html', username=current_user)

### ----- Endpoints ----- ###

# Endpoint para obtener el tipo de un Pokemon segun su nombre
@app.route('/pokemon/type/<nombre>', methods=['POST'])
@login_required
def get_pokemon_type(nombre):
    nombre = request.form['nombre']
    # Consultamos si existe el Pokemon con ese nombre
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{nombre.lower()}')
    if response.status_code == 200:
        pokemon_data = response.json()
        types = [type_data['type']['name'] for type_data in pokemon_data['types']]
        tipo = types[0]
        return render_template('consulta.html', pokemon_name=nombre, pokemon_types=tipo)
    else:
        return jsonify({'error': 'Pokemon no encontrado'}), 404

# Endpoint para obtener un Pokemon al azar de un tipo/clase especifico
@app.route('/pokemon/random/<tipo>', methods=['POST'])
@login_required
def get_random_pokemon(tipo):
    tipo = request.form['tipo']
    # Consultamos si existe el tipo de Pokemon con ese nombre
    response = requests.get(f'https://pokeapi.co/api/v2/type/{tipo.lower()}')
    if response.status_code == 200:
        type_data = response.json()
        pokemon_nombre = [pokemon['pokemon']['name'] for pokemon in type_data['pokemon']]
        #return jsonify({'type': tipo, 'random_pokemon': random.choice(pokemon_nombre)}) #Usando random elegimos el nombre de un pokemos al azar
        return render_template('consulta.html', random_pokemon=random.choice(pokemon_nombre))
    else:
        return jsonify({'error': 'Tipo no encontrado'}), 404
    
# Endpoint para obtener el Pokemon con nombre mas largo segun tipo indicado
@app.route('/pokemon/longest/<tipo>', methods=['POST'])
@login_required
def get_longest_pokemon_name(tipo):
    tipo = request.form['tipo']
    response = requests.get(f'https://pokeapi.co/api/v2/type/{tipo.lower()}')
    if response.status_code == 200:
        type_data = response.json()
        longest_name = max(type_data['pokemon'], key=lambda x: len(x['pokemon']['name']))['pokemon']['name']
        #return jsonify({'type': tipo, 'longest_name': longest_name})
        return render_template('consulta.html', longest_name=longest_name)
    else:
        return jsonify({'error': 'Tipo no encontrado'}), 404


# Endpoint para obtener un Pokemon al azar que contenga alguna de las letras 'I','A' o 'M' y que sea del tipo específico más fuerte en base al clima actual de tu ciudad
@app.route('/pokemon/random/condicion', methods=['POST'])
@login_required
def get_random_pokemon_condicion():

    # Obtener el clima actual
    latitud, longitud = obtener_coordenadas()
    temperatura = obtener_temperatura_actual(latitud, longitud)

    # Determinar el tipo de Pokemon mas fuerte segun el clima
    tipo_mas_fuerte = get_tipo_mas_fuerte_segun_clima(temperatura)

    # Hacer la solicitud a la Poke API para obtener todos los Pokemon del tipo mas fuerte
    response = requests.get(f"https://pokeapi.co/api/v2/type/{tipo_mas_fuerte}")
    if response.status_code == 200:
        data = response.json()
        pokemons = [pokemon['pokemon']['name'] for pokemon in data['pokemon']]        
        # Filtrar los Pokemon que contienen alguna de las letras 'I', 'A', 'M' en su nombre
        filtered_pokemons = [pokemon for pokemon in pokemons if any(letter in pokemon for letter in ['i', 'a', 'm'])]        
        # Comprobamos si hay algun valor en la lista
        if filtered_pokemons:
            random_pokemon = random.choice(filtered_pokemons)
            #return jsonify({'random_pokemon_condicion': random_pokemon})
            return render_template('consulta.html', random_pokemon_condicion=random_pokemon)
        else:
            return jsonify({'error': 'No se encontro Pokemon que coincida con la condicion'}), 404

    else:
        return jsonify({'error': 'Error al obtener el Pokemon'}), 500

if __name__ == "__main__":
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.register_error_handler(405, status_405)
    app.run(host="0.0.0.0", port=5000, debug=True)
    