from flask import Flask, jsonify
import requests
import random

app = Flask(__name__)

### ----- Endpoints ----- ###

# Endpoint para obtener el tipo de un Pokemon segun su nombre
@app.route('/pokemon/type/<nombre>')
def get_pokemon_type(nombre):
    # Consultamos si existe el Pokemon con ese nombre
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{nombre.lower()}')
    if response.status_code == 200:
        pokemon_data = response.json()
        types = [type_data['type']['name'] for type_data in pokemon_data['types']]
        return jsonify({'name': nombre, 'types': types})
    else:
        return jsonify({'error': 'Pokemon no encontrado'}), 404

# Endpoint para obtener un Pokemon al azar de un tipo/clase especifico
@app.route('/pokemon/random/<tipo>')
def get_random_pokemon(tipo):
    # Consultamos si existe el tipo de Pokemon con ese nombre
    response = requests.get(f'https://pokeapi.co/api/v2/type/{tipo.lower()}')
    if response.status_code == 200:
        type_data = response.json()
        pokemon_nombre = [pokemon['pokemon']['name'] for pokemon in type_data['pokemon']]
        return jsonify({'type': tipo, 'random_pokemon': random.choice(pokemon_nombre)}) #Usando random elegimos el nombre de un pokemos al azar
    else:
        return jsonify({'error': 'Tipo no encontrado'}), 404
    
# Endpoint para obtener el Pokemon con nombre mas largo segun tipo indicado
@app.route('/pokemon/longest/<tipo>')
def get_longest_pokemon_name(tipo):
    response = requests.get(f'https://pokeapi.co/api/v2/type/{tipo.lower()}')
    if response.status_code == 200:
        type_data = response.json()
        longest_name = max(type_data['pokemon'], key=lambda x: len(x['pokemon']['name']))['pokemon']['name']
        return jsonify({'type': tipo, 'longest_name': longest_name})
    else:
        return jsonify({'error': 'Tipo no encontrado'}), 404

# Endpoint para obtener un Pokemon al azar que contenga alguna de las letras 'I','A' o 'M' y que sea del tipo específico más fuerte en base al clima actual de tu ciudad
# #### FALTA CONDICION DEL CLIMA ####
@app.route('/pokemon/random/condicion/<tipo>')
def get_random_pokemon_condicion(tipo):
    response = requests.get(f"https://pokeapi.co/api/v2/type/{tipo.lower()}")
    if response.status_code == 200:
        data = response.json()
        pokemons = [pokemon['pokemon']['name'] for pokemon in data['pokemon']]        
        # Filtrar los Pokemon que contienen alguna de las letras 'I', 'A', 'M' en su nombre
        filtered_pokemons = [pokemon for pokemon in pokemons if any(letter in pokemon for letter in ['i', 'a', 'm'])]        
        # Comprobamos si hay algun valor en la lista
        if filtered_pokemons:
            random_pokemon = random.choice(filtered_pokemons)
            return jsonify({'random_pokemon_condition': random_pokemon})
        else:
            return jsonify({'error': 'No se encontro Pokemon que coincida con la condicion'}), 404

    else:
        return jsonify({'error': 'Error al obtener el Pokemon'}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)