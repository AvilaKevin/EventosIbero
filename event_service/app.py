from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson.objectid import ObjectId

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Se crea la conexion a mongo
cliente = MongoClient("mongodb://mongodb:27017")
# Se crea la db
db = cliente["eventos_db"]
# crea una coleccion de la base datos
coleccion = db["eventos"]
# Se crean todas las funciones

# Este trae los eventos
@app.get("/eventos")
async def obtener_eventos ():
    eventos = []
    for evento in coleccion.find():
        evento["_id"] = str(evento["_id"])
        eventos.append(evento)
        return eventos
    
# Este colocala los eventos
@app.put("/eventos/{evento_id}")
async def editar_evento(evento_id: str, nombre: str, fecha:str, lugar:str):
    resultado = coleccion. update_one(
        {"_id": ObjectId(evento_id)},
        {"$set":{"nombre":nombre, "fecha": fecha, "lugar":lugar}}
    )
    if resultado.matched_count ==0:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return{"estado":"actualizado"}

# Este elimina los eventos
@app.delete("/eventos/{evento_id}")
async def eliminar_evento(evento_id: str):
    resultado = coleccion.delete_one({"_id": ObjectId(evento_id)})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404,detail="Evento no encontrado")
    return{"estado":"eliminado"}

@app.post("/eventos")
async def crear_evento(nombre: str, fecha:str, lugar:str):
    evento = {"nombre": nombre, "fecha": fecha, "lugar": lugar}
    resultado = coleccion.insert_one(evento)
    evento["_id"] = str(resultado.inserted_id)
    return evento