# Importamos las librerías
import psutil
import platform
import os
import json
from datetime import datetime

# En esta parte se crea un diccionario donde se almacenarán los datos con sus respectivas claves-valores
def obtener_datos():
    datos = {}

    # Bloque de obtención del estado de la batería
    try:
        bateria = psutil.sensors_battery()
        if bateria:
            datos["bateria"] = bateria.percent       
            datos["cargando"] = bateria.power_plugged
        else:
            datos["bateria"] = None
            datos["cargando"] = None
    except:
        datos["bateria"] = None
        datos["cargando"] = None

    # Obtención de la memoria RAM
    mem = psutil.virtual_memory()
    datos["ram"] = mem.percent   

    # Obtención del disco (unidad C:\ en nuestro dispositivo Windows)
    disco = psutil.disk_usage('C:\\')
    datos["disco"] = disco.percent   

    # Obtención de la red (hacemos ping a Google para probar conectividad)
    response = os.system("ping -n 1 google.com >nul 2>&1")
    datos["red"] = "Conectado" if response == 0 else "Sin conexión"

    # Obtención del sistema operativo y su versión
    datos["sistema"] = platform.system() + " " + platform.release()

    return datos

# Llamamos método obtener_datos() y guardamos su resultado
def diagnosticar_pc():
    datos = obtener_datos()
    diagnostico = ""

    # Reglas IF–THEN
    if datos["bateria"] is not None:
        if datos["bateria"] < 10 and not datos["cargando"]:
            diagnostico = "⚠️ Posible problema de batería: carga muy baja y no conectado al cargador."
        elif datos["bateria"] == 100 and datos["cargando"]:
            diagnostico = "ℹ️ La batería está totalmente cargada y conectada al cargador."

    if datos["ram"] > 90:
        diagnostico = "⚠️ La memoria RAM está muy saturada, posible problema de rendimiento."

    if datos["disco"] > 90:
        diagnostico = "⚠️ El disco está casi lleno, puede causar lentitud."

    if datos["red"] == "Sin conexión":
        diagnostico = "⚠️ No hay conexión a internet. Revisa el adaptador de red o la configuración."

    if diagnostico == "":
        diagnostico = "✅ No se detectaron fallas graves en el sistema."

    # Guardar en JSON
    guardar_json(datos, diagnostico)

    return diagnostico

# Función para guardar los resultados en un archivo JSON
def guardar_json(datos, diagnostico):
    registro = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "datos": datos,
        "diagnostico": diagnostico
    }

    # Nombre del archivo
    archivo = "diagnostico_pc.json"

    # Si el archivo ya existe, cargamos los datos previos y añadimos el nuevo
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            historial = json.load(f)
    except FileNotFoundError:
        historial = []

    historial.append(registro)

    # Guardamos de nuevo el historial completo
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(historial, f, indent=4, ensure_ascii=False)

# Ejecución principal
if __name__ == "__main__":
    resultado = diagnosticar_pc()
    print(resultado)
    print("✅ Los resultados fueron guardados en 'diagnostico_pc.json'")

