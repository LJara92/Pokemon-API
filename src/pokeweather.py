from flask import Flask, jsonify

app = Flask(__name__)

### ----- Endpoints ----- ###

# Endpoint para obtener el tipo de un Pokemon segun su nombre
@app.route('/pokemon/type/<nombre>')
def get_pokemon_type(nombre):
    pass

# Endpoint para obtener un Pokemon al azar de un tipo/clase especifico
@app.route('/pokemon/random/<tipo>')
def get_random_pokemon(tipo):
    pass
    
# Endpoint para obtener el Pokemon con nombre mas largo segun tipo indicado
@app.route('/pokemon/longest/<tipo>')
def get_longest_pokemon_name(tipo):
    pass

# Endpoint para obtener un Pokemon al azar que contenga alguna de las letras 'I','A' o 'M' y que sea del tipo específico más fuerte en base al clima actual de tu ciudad
@app.route('/pokemon/random/condicion')
def get_random_pokemon_condicion():
    pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)