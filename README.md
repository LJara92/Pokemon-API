# Pokeweather

## Descripción del Proyecto

Pokeweather es una API desarrollada para un desafío de una entrevista de Mercado Libre, que interactúa con la API pública de Pokémon (pokeapi.co) para consultar ciertos endpoints y añade un sistema de autenticación.

## Tabla de Contenidos

- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Endpoints](#endpoints)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)
- [Contacto](#contacto)

## Requisitos

Antes de comenzar, asegúrate de tener instalados los siguientes componentes:

- Python 3.x
- Flask

## Instalación

Sigue estos pasos para configurar el proyecto en tu entorno local:

1. Clona este repositorio:

   ```bash
   git clone https://github.com/LJara92/Pokemon-API.git
   ```

2. Accede al directorio del proyecto:

   ```bash
   cd Pokemon-API
   ```

3. Instala las dependencias necesarias:

   ```bash
   pip install -r requirements.txt
   ```

## Uso

Para ejecutar la API, realiza lo siguiente:

1. Inicia la aplicación:

   ```bash
   python src/pokeweather-auth-login.py
   ```

2. Accede a la API a través de tu navegador web en la dirección `http://localhost:5000`.

3. Inicia sesión con las siguientes credenciales:

   - **Administrador:**
     - Usuario: admin
     - Contraseña: admin123
   - **Usuario:**
     - Usuario: user
     - Contraseña: user123

   > **Nota:** Es obligatorio iniciar sesión para acceder a los endpoints.

## Endpoints

La API ofrece los siguientes endpoints:

- `POST /pokemon/type/<nombre>`: Obtiene el tipo de un Pokémon según su nombre.
- `POST /pokemon/random/<tipo>`: Obtiene un Pokémon al azar de un tipo específico.

## Tecnologías Utilizadas

- Python
- Flask
- PokeAPI (https://pokeapi.co/)

## Contribuciones

Las contribuciones son bienvenidas. Si deseas colaborar, por favor sigue estos pasos:

1. Haz un fork del proyecto.
2. Crea una nueva rama para tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus modificaciones y haz commit de los cambios (`git commit -m 'Añadir nueva funcionalidad'`).
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Abre una Pull Request.

## Licencia

Este proyecto está bajo la Licencia MIT.

## Contacto

Para consultas o más información, puedes contactarme a través de:

- Correo electrónico: [jara.lautaro@gmail.com](mailto:jara.lautaro@gmail.com)
- LinkedIn: [Lautaro Jara](https://www.linkedin.com/in/lautaro-jara/)
