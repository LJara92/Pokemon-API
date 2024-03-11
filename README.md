# Pokeweather
## MELI Challenge
Este challenge consiste en crear una API que consulte a la API publica de Pokemon (pokeapi.co) ciertos endpoints y agregar un sistema de autenticacion

## Requisitos
- Python
- Flask

## Instalacion
1. Realizar una copia del repositorio

```bash
git clone https://github.com/LJara92/Pokemon-API.git

cd Pokemon-API
```
2. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Uso

1. Ejecutar la API

```bash
python src/pokeweather-auth-login.py
```

2. Accede a la API en tu navegador web utilizando la direccion `http://localhost:5000`

3. Inicia sesion con las credenciales
```bash
User: admin
Password: admin123

---------------------

User: user
Password: user123
```

4. Una vez dentro, vas a poder acceder a diferentes endpoints desde la pagina de inicio

** No se podra acceder a los endpoints si no estas logueado **

## Endpoints

- `/pokemon/type/<nombre>` (POST): Obtiene el tipo de un Pokemon segun su nombre
- `/pokemon/random/<tipo>` (POST): Obtiene un Pokemon al azar de un tipo especifico
- `/pokemon/longest/<tipo>` (POST): Obtiene el Pokemon con el nombre mas largo segun un tipo dado
- `/pokemon/random/condicion` (POST): Obtiene un Pokemon al azar que cumpla cierta condicion climatica y ciertas letras en el nombre

