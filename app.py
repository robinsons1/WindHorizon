from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Montar carpeta static para servir index.html
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("app/static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/api/sensores")
async def get_sensores():
    # Datos de ejemplo
    ejemplo = {
        "timestamp1": 12,
        "timestamp2": 15,
        "timestamp3": 10
    }
    return ejemplo
