#Aqui importamos las librerias
import psutil
import platform
import os

#En esta parte se crea un diccionario donde se almacenara los datos con su respectivas claves-valores
def obtener_datos():
    datos = {}

    # Bloque de obtencion del estado de la batería
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

    # Obtencion de la memoria RAM
    mem = psutil.virtual_memory()
    datos["ram"] = mem.percent   

    # Obtencion del disco (unidad C:\ en nuestro dispositivo Windows)
    disco = psutil.disk_usage('C:\\')
    datos["disco"] = disco.percent   

    # Obtencion de la red (hacemos ping a Google para probar conectividad)
    response = os.system("ping -n 1 google.com >nul 2>&1")
    datos["red"] = "Conectado" if response == 0 else "Sin conexión"

    # Obtencion del sistema operativo y su version
    datos["sistema"] = platform.system() + " " + platform.release()

    return datos

#Llamamos método obtener_datos() y guardamos su resultado
def diagnosticar_pc():
    datos = obtener_datos()
    print("Datos detectados:", datos)

    # Reglas IF–THEN
    if datos["bateria"] is not None:
        if datos["bateria"] < 10 and not datos["cargando"]:
            return "⚠️ Posible problema de batería: carga muy baja y no conectado al cargador."
        elif datos["bateria"] == 100 and datos["cargando"]:
            return "ℹ️ La batería está totalmente cargada y conectada al cargador."

    if datos["ram"] > 90:
        return "⚠️ La memoria RAM está muy saturada, posible problema de rendimiento."

    if datos["disco"] > 90:
        return "⚠️ El disco está casi lleno, puede causar lentitud."

    if datos["red"] == "Sin conexión":
        return "⚠️ No hay conexión a internet. Revisa el adaptador de red o la configuración."

    return "✅ No se detectaron fallas graves en el sistema."

# Ejecución principal
if __name__ == "__main__":
    print(diagnosticar_pc())
