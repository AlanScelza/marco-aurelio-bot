# Marco Aurelio Bot

Bot de Telegram que envia una meditacion aleatoria.

## Requisitos

- Python 3.10+
- MongoDB
- Token de bot de Telegram

## Configuracion rapida

1. Copia variables de entorno:

```bash
cp .env.example .env
```

2. Completa el token en `.env`.

3. Inicia con Docker:

```bash
docker compose up --build
```

## Variables de entorno

- `BOT_TOKEN`: token del bot de Telegram.
- `STORAGE_TYPE`: nombre de la clase de storage (por ejemplo `MongoStorage`).
- `MONGO_STORAGE_URL`: URL de MongoDB.
- `MONGO_STORAGE_DB`: nombre de la base.
- `MONGO_STORAGE_COLLECTION`: nombre de la coleccion.

## Setup Inicial 

Luego de descargar las meditaciones, deben ser convertidas a `txt` y procesadas de manera que queden:
```
LIBRO <X>

Med1

Med2

MedN
```

Para levantar:
```
# Levantar los contenedores
docker compose up -d
```
```
# Copiar archivos para cargar meditaciones
docker cp meditaciones.txt marco-aurelio:/
docker cp charge_meditations.txt marco-aurelio:/
```
```
# Cargar meditaciones
docker exec -ti marco-aurelio sh
```
```
python3 charge_meditations.txt
```

## Privacidad

- No se persisten datos de usuarios.
- Los logs no incluyen identificadores personales.

## Contenido (Meditaciones)

Fuente utilizada: https://freeditorial.com/es/books/meditaciones-de-marco-aurelio
La pagina indica que el material fue subido como dominio publico; este proyecto asume esa declaracion y no garantiza el estatus legal del texto.

## Licencia

El codigo se distribuye bajo licencia MIT. Ver `LICENSE`.
