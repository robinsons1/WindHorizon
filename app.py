import asyncio
import random
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import firebase_admin
from firebase_admin import credentials, firestore

app = FastAPI()

# Montar carpeta estática y templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

db = firestore.client()

sensores = {
    "voltaje_dc": (10, 14),
    "corriente_bateria": (0, 30),
    "corriente_inversor": (0, 50),
    "rpm_turbina": (0, 3000),
    "vibracion": (0, 10),
    "humedad": (20, 80),
    "temperatura": (0, 40)
}

async def subir_datos_periodicos():
    while True:
        datos = {}
        for sensor, (min_val, max_val) in sensores.items():
            datos[sensor] = round(random.uniform(min_val, max_val), 2)
        datos["timestamp"] = firestore.SERVER_TIMESTAMP

        db.collection("sensores").add(datos)
        print("Datos subidos:", datos)

        await asyncio.sleep(60)  # espera 60 segundos

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(subir_datos_periodicos())
