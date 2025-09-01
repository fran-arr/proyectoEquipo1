import psutil, platform, os

def obtener_datos():
    datos = {}

    # Estado de la batería
    try:
        bateria = psutil.sensors_battery()
        if bateria:
            datos["bateria"] = bateria.percent       # porcentaje (float)
            datos["cargando"] = bateria.power_plugged
        else:
            datos["bateria"] = None
            datos["cargando"] = None
    except:
        datos["bateria"] = None
        datos["cargando"] = None

    # Memoria RAM
    mem = psutil.virtual_memory()
    datos["ram"] = mem.percent   # porcentaje (float)

    # Disco
    disco = psutil.disk_usage('/')
    datos["disco"] = disco.percent   # porcentaje (float)

    # Red (hacemos ping a Google para probar conectividad)
    if platform.system().lower() == "windows":
        response = os.system("ping -n 1 google.com >nul 2>&1")
    else:
        response = os.system("ping -c 1 google.com > /dev/null 2>&1")
    datos["red"] = "Conectado" if response == 0 else "Sin conexión"

    # Sistema
    datos["sistema"] = platform.system() + " " + platform.release()

    return datos


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
