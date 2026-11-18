[![CI](https://github.com/carlomederos/Juegos/actions/workflows/ci.yml/badge.svg)](https://github.com/carlomederos/Juegos/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/carlomederos/Juegos/branch/master/graph/badge.svg)](https://codecov.io/gh/carlomederos/Juegos)

# Pruebas unitarias de la aplicación de videojuegos

## Cobertura

- `test_models.py`: creación y campos de `Juego`, operaciones de los controladores y restricción de nombre obligatorio.
- `test_routes.py`: páginas públicas de acceso, protección de la lista y formulario, y respuesta 404.
- `test_api.py`: listado, creación, consulta, actualización, eliminación, validación y recurso inexistente en `/api/juegos`.

## Entorno y ejecución

Las pruebas estan escritas con `unittest` y se ejecutan con `pytest`. Usan SQLite en memoria (lo configura `tests/conftest.py`), asi que no tocan la base de MySQL. Desde la carpeta raíz del proyecto, activa el entorno virtual y ejecuta:

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt pytest pytest-cov
python -m pytest --cov=. tests/
```

La salida de la ejecución se guarda en `results.txt`.

## Integracion continua

Cada push o pull request ejecuta el workflow `.github/workflows/ci.yml` en GitHub Actions: instala las dependencias, corre las pruebas con cobertura y sube el reporte a Codecov.

## Retos y soluciones

La aplicación existente crea una instancia Flask global y configura MySQL directamente; no tiene una factoría `create_app`. Las pruebas configuran SQLite en memoria antes de la primera conexión, usan contexto de aplicación y limpian las tablas en cada prueba. Para rutas protegidas se crea un usuario de prueba y se prepara la sesión del cliente de Flask.
