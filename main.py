
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field

app = FastAPI()

# ---------------------- MODELOS ----------------------

class Moto(BaseModel):
    marca: str = Field(..., min_length=1, max_length=50, description="Marca de la moto")
    modelo: str = Field(..., min_length=1, max_length=50, description="Modelo de la moto")
    cilindraje: int = Field(..., gt=0, lt=3000, description="Cilindraje en cc (1-2999)")

class CasaEmpeño(BaseModel):
    nombre: str
    direccion: str
    tipo_producto: str

class Concierto(BaseModel):
    artista: str
    lugar: str
    fecha: str

class Netflix(BaseModel):
    titulo: str
    genero: str

class Compra(BaseModel):
    producto: str
    valor: float
    iva: float = 0.19

class VideoJuegos(BaseModel):
    nombre_tienda: str
    direccion: str
    precio_hora: float
    jornada_horas: int

class MascotaEnferma(BaseModel):
    nombre_mascota: str
    tipo_animal: str
    edad: int
    sintomas: str
    gravedad: str  # leve, moderada, grave
    nombre_dueño: str


# ---------------------- ENDPOINTS ----------------------

# Root endpoint
@app.get("/")
def root():
    return {"message": "¡FastAPI funcionando correctamente!", "endpoints": "Ve a /docs para ver la documentación"}

# 1. Capturar moto + id mecánico (path)
@app.post("/moto/{id_mecanico}")
def crear_moto(
    moto: Moto,
    id_mecanico: int = Path(..., gt=0, description="ID del mecánico (entero > 0)")
):
    return {"moto": moto, "id_mecanico": id_mecanico}

# Variante con parámetros por query (para capturar cada campo por separado en Swagger)
@app.post("/moto_q/{id_mecanico}")
def crear_moto_query(
    id_mecanico: int = Path(..., gt=0, description="ID del mecánico (entero > 0)"),
    marca: str = Query(..., min_length=1, max_length=50, description="Marca de la moto"),
    modelo: str = Query(..., min_length=1, max_length=50, description="Modelo de la moto"),
    cilindraje: int = Query(..., gt=0, lt=3000, description="Cilindraje en cc (1-2999)")
):
    moto = {"marca": marca, "modelo": modelo, "cilindraje": cilindraje}
    return {"moto": moto, "id_mecanico": id_mecanico}

# 2. Captura casa de empeño + sede
@app.post("/casa_empeno/{id_sede}")
def crear_casa(casa: CasaEmpeño, id_sede: int):
    return {"casa": casa, "id_sede": id_sede}

# Variante por query
@app.post("/casa_empeno_q/{id_sede}")
def crear_casa_query(
    id_sede: int = Path(..., gt=0),
    nombre: str = Query(..., min_length=1, max_length=80),
    direccion: str = Query(..., min_length=1, max_length=120),
    tipo_producto: str = Query(..., min_length=1, max_length=50)
):
    casa = {"nombre": nombre, "direccion": direccion, "tipo_producto": tipo_producto}
    return {"casa": casa, "id_sede": id_sede}

# 3. Concierto + boleta
@app.post("/concierto/{codigo_boleta}")
def crear_concierto(concierto: Concierto, codigo_boleta: str):
    return {"concierto": concierto, "codigo_boleta": codigo_boleta}


@app.post("/concierto_q/{codigo_boleta}")
def crear_concierto_query(
    codigo_boleta: str = Path(..., min_length=1),
    artista: str = Query(..., min_length=1, max_length=80),
    lugar: str = Query(..., min_length=1, max_length=120),
    fecha: str = Query(..., min_length=1)
):
    concierto = {"artista": artista, "lugar": lugar, "fecha": fecha}
    return {"concierto": concierto, "codigo_boleta": codigo_boleta}

# 4. Netflix favorito + código
@app.post("/netflix/{codigo}")
def crear_netflix(serie: Netflix, codigo: str):
    return {"serie": serie, "codigo": codigo}

# Variante por query
@app.post("/netflix_q/{codigo}")
def crear_netflix_query(
    codigo: str = Path(..., min_length=1),
    titulo: str = Query(..., min_length=1, max_length=120),
    genero: str = Query(..., min_length=1, max_length=50)
):
    serie = {"titulo": titulo, "genero": genero}
    return {"serie": serie, "codigo": codigo}

# 5. Sumatoria de 4 datos
@app.get("/sumatoria")
def sumatoria(a: int, b: int, c: int, d: int):
    return {"resultado": a + b + c + d}

# 6. Calculo de dólares y reales
@app.get("/convertir")
def convertir(valor_cop: float):
    dolar = valor_cop / 4200   # ejemplo 1 USD ≈ 4200 COP
    real = valor_cop / 800     # ejemplo 1 BRL ≈ 800 COP
    return {"COP": valor_cop, "USD": round(dolar, 2), "BRL": round(real, 2)}

# 7. Calculo IVA
@app.post("/compra/")
def calcular_iva(compra: Compra):
    total = compra.valor * (1 + compra.iva)
    return {"producto": compra.producto, "valor_total": round(total, 2)}

# Variante por query
@app.post("/compra_q/")
def calcular_iva_query(
    producto: str = Query(..., min_length=1, max_length=120),
    valor: float = Query(..., gt=0),
    iva: float = Query(0.19, ge=0.0, le=1.0, description="IVA en proporción (0-1)")
):
    total = valor * (1 + iva)
    return {"producto": producto, "valor_total": round(total, 2)}

# 8. Cervezas y Bo' Rai Cho
@app.get("/cervezas")
def cervezas(cantidad: int, etiqueta: str):
    limite = 5
    mensaje = None
    if cantidad > limite:
        mensaje = f"Bo' Rai Cho dice: ¡Te pasaste con el {etiqueta}! 🍻"
    return {"cervezas": cantidad, "etiqueta": etiqueta, "mensaje": mensaje}

# 9. Tienda de videojuegos (alquiler PC gamers)
@app.post("/tienda_videojuegos/")
def tienda_videojuegos(tienda: VideoJuegos):
    total = tienda.precio_hora * tienda.jornada_horas
    return {
        "tienda": tienda.nombre_tienda,
        "direccion": tienda.direccion,
        "total_jornada": total
    }

# Variante por query
@app.post("/tienda_videojuegos_q/")
def tienda_videojuegos_query(
    nombre_tienda: str = Query(..., min_length=1, max_length=80),
    direccion: str = Query(..., min_length=1, max_length=120),
    precio_hora: float = Query(..., gt=0),
    jornada_horas: int = Query(..., gt=0, lt=24)
):
    total = precio_hora * jornada_horas
    return {
        "tienda": nombre_tienda,
        "direccion": direccion,
        "total_jornada": total
    }

# 10. Capturar datos de mascota enferma + ID veterinario
@app.post("/mascota_enferma/{id_veterinario}")
def crear_mascota_enferma(mascota: MascotaEnferma, id_veterinario: int):
    # Determinar urgencia basada en la gravedad
    urgencia = "URGENTE" if mascota.gravedad == "grave" else "NORMAL"
    
    return {
        "mascota": mascota,
        "id_veterinario": id_veterinario,
        "urgencia": urgencia,
        "mensaje": f"Registro creado para {mascota.nombre_mascota} con veterinario ID {id_veterinario}"
    }

# Variante por query
@app.post("/mascota_enferma_q/{id_veterinario}")
def crear_mascota_enferma_query(
    id_veterinario: int = Path(..., gt=0),
    nombre_mascota: str = Query(..., min_length=1, max_length=60),
    tipo_animal: str = Query(..., min_length=1, max_length=40),
    edad: int = Query(..., ge=0, lt=50),
    sintomas: str = Query(..., min_length=1, max_length=200),
    gravedad: str = Query(..., description="leve | moderada | grave"),
    nombre_dueño: str = Query(..., min_length=1, max_length=60)
):
    urgencia = "URGENTE" if gravedad == "grave" else "NORMAL"
    mascota = {
        "nombre_mascota": nombre_mascota,
        "tipo_animal": tipo_animal,
        "edad": edad,
        "sintomas": sintomas,
        "gravedad": gravedad,
        "nombre_dueño": nombre_dueño,
    }
    return {
        "mascota": mascota,
        "id_veterinario": id_veterinario,
        "urgencia": urgencia,
        "mensaje": f"Registro creado para {nombre_mascota} con veterinario ID {id_veterinario}"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
