# Conversor de Divisas con datos del Banco Central Europeo (BCE)
# Módulo 486 - Acceso a Datos
#
# Pasos del programa:
#   1. API  -> descargar el XML del BCE con requests
#   2. XML  -> leer la fecha y las tasas con ElementTree
#   3. GUI  -> ventana Tkinter para convertir importes

import requests
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import ttk, messagebox

URL_BCE = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"


# ---------------------------------------------------------------
# 1. API: descargar el XML
# ---------------------------------------------------------------
def descargar_xml():
    """Hace una petición GET al BCE y devuelve el XML como texto."""
    respuesta = requests.get(URL_BCE, timeout=10)

    if respuesta.status_code != 200:
        raise Exception("El servidor respondió con código " + str(respuesta.status_code))

    return respuesta.content.decode("utf-8")


# ---------------------------------------------------------------
# 2. XML: sacar la fecha y las tasas
# ---------------------------------------------------------------
def leer_tasas(texto_xml):
    """Recorre el XML y devuelve (fecha, diccionario de tasas)."""
    raiz = ET.fromstring(texto_xml)

    fecha = ""
    tasas = {"EUR": 1.0}  # El euro no viene en el XML: lo añadimos a mano

    # root.iter() recorre TODAS las etiquetas del árbol, una a una
    for elemento in raiz.iter():
        # El <Cube> que tiene el atributo "time" guarda la fecha
        if "time" in elemento.attrib:
            fecha = elemento.attrib["time"]

        # Los <Cube> con "currency" y "rate" son las monedas
        if "currency" in elemento.attrib:
            moneda = elemento.attrib["currency"]
            tasa = float(elemento.attrib["rate"])
            tasas[moneda] = tasa

    return fecha, tasas


# ---------------------------------------------------------------
# Lógica de cálculo: conversión cruzada usando el euro como puente
# ---------------------------------------------------------------
def convertir(importe, tasa_origen, tasa_destino):
    """
    Primero pasamos el importe a euros (importe / tasa_origen)
    y luego de euros a la moneda destino (* tasa_destino).
    """
    en_euros = importe / tasa_origen
    return en_euros * tasa_destino


# ---------------------------------------------------------------
# 3. GUI: la ventana
# ---------------------------------------------------------------
def al_pulsar_convertir():
    """Se ejecuta cuando el usuario pulsa el botón 'Convertir'."""
    texto = entrada_importe.get().replace(",", ".")  # aceptamos 10,5 y 10.5

    # Validación: si escribe letras, float() da error
    try:
        importe = float(texto)
    except ValueError:
        messagebox.showerror("Error", "Introduce un número válido (ej: 100 o 25.50)")
        return

    origen = combo_origen.get()
    destino = combo_destino.get()

    resultado = convertir(importe, tasas[origen], tasas[destino])
    etiqueta_resultado.config(text=f"{importe:.2f} {origen} = {resultado:.2f} {destino}")


# --- Carga automática al iniciar ---
try:
    xml_texto = descargar_xml()
    fecha, tasas = leer_tasas(xml_texto)
except Exception as error:
    # Si no hay internet o falla el BCE, avisamos y cerramos
    messagebox.showerror("Error de conexión", f"No se pudieron descargar los datos:\n{error}")
    raise SystemExit

monedas = sorted(tasas.keys())  # lista ordenada alfabéticamente para los desplegables

# --- Ventana principal ---
ventana = tk.Tk()
ventana.title("Conversor de Divisas (BCE)")
ventana.geometry("380x300")

tk.Label(ventana, text="Conversor de Divisas", font=("Arial", 16, "bold")).pack(pady=10)
tk.Label(ventana, text=f"Datos del BCE actualizados el: {fecha}", fg="gray").pack()

# Campo numérico para el importe
tk.Label(ventana, text="Cantidad:").pack(pady=(10, 0))
entrada_importe = tk.Entry(ventana, justify="center")
entrada_importe.insert(0, "100")
entrada_importe.pack()

# Desplegable moneda de origen
tk.Label(ventana, text="De:").pack()
combo_origen = ttk.Combobox(ventana, values=monedas, state="readonly")
combo_origen.set("EUR")
combo_origen.pack()

# Desplegable moneda de destino
tk.Label(ventana, text="A:").pack()
combo_destino = ttk.Combobox(ventana, values=monedas, state="readonly")
combo_destino.set("USD")
combo_destino.pack()

# Botón que dispara el cálculo
tk.Button(ventana, text="Convertir", command=al_pulsar_convertir).pack(pady=10)

# Etiqueta donde sale el resultado
etiqueta_resultado = tk.Label(ventana, text="", font=("Arial", 13, "bold"), fg="blue")
etiqueta_resultado.pack()

ventana.mainloop()  # deja la ventana abierta esperando clics
