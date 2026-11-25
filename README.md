# PrDesafio03 – Conversor de Divisas (BCE)

Módulo 486 – Acceso a Datos (Python).

Aplicación de escritorio en **Tkinter** que, al arrancar, descarga los tipos de cambio diarios del
[Banco Central Europeo](https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml) en XML,
los procesa con `xml.etree.ElementTree` y permite convertir importes entre cualquier par de monedas.

## Cómo ejecutarlo

```bash
pip install -r requirements.txt
python conversor_divisas.py
```

## Funcionamiento

| Parte | Función | Qué hace |
|---|---|---|
| API | `descargar_xml()` | Petición GET con `requests` y comprobación del `status_code` |
| XML | `leer_tasas()` | Recorre el árbol y saca la fecha (`time`) y las monedas (`currency`, `rate`) |
| Cálculo | `convertir()` | Conversión cruzada usando el euro como puente |
| GUI | `al_pulsar_convertir()` | Valida el importe y muestra el resultado |

**Fórmula:** `CantidadFinal = (Importe / TasaOrigen) × TasaDestino`

El XML no incluye el euro (todas las tasas son "1 EUR = X"), así que se añade a mano con tasa `1.0`.

Autor: Isaac Trujillo Bombin
