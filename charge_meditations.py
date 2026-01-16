from pymongo import MongoClient

# Conectar a MongoDB
client = MongoClient("mongodb://mongo:27017/")
db = client["meditaciones"]
collection = db["meditaciones"]

# Leer el archivo
with open("meditaciones.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

# Variables para almacenar los datos
libro = None
meditaciones = []
current_meditacion = None
current_text = []

for line in lines:
    line = line.strip()
    
    if line.startswith("LIBRO"):
        # Si hay una meditación en curso, guárdala antes de empezar un nuevo libro
        if current_meditacion:
            meditacion = {
                "_id": len(meditaciones) + 1,
                "libro": libro,
                "numero": current_meditacion,
                "texto": " ".join(current_text).strip()
            }
            meditaciones.append(meditacion)
            current_meditacion = None
            current_text = []
        
        # Actualizar el libro actual
        libro = line
    
    elif line and line[0].isdigit():
        # Si hay una meditación en curso, guárdala antes de empezar una nueva
        if current_meditacion:
            meditacion = {
                "_id": len(meditaciones) + 1,
                "libro": libro,
                "numero": current_meditacion,
                "texto": " ".join(current_text).strip()
            }
            meditaciones.append(meditacion)
        
        # Iniciar una nueva meditación
        current_meditacion, new_text = line.split(".", 1)
        current_meditacion = int(current_meditacion.strip())
        current_text = [new_text.strip()]
    
    else:
        # Continuar agregando líneas a la meditación actual
        if current_text is not None:
            current_text.append(line)

# Agregar la última meditación si existe
if current_meditacion:
    meditacion = {
        "_id": len(meditaciones) + 1,
        "libro": libro,
        "numero": current_meditacion,
        "texto": " ".join(current_text).strip()
    }
    meditaciones.append(meditacion)

# Insertar las meditaciones en la base de datos
if meditaciones:
    collection.insert_many(meditaciones)
    print("Meditaciones cargadas en MongoDB.")
else:
    print("No se encontraron meditaciones válidas.")
