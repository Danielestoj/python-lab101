import json
from datetime import datetime

def cargar_ventas(ruta_archivo):
    """Lee el archivo JSON y devuelve la lista de ventas."""
    with open(ruta_archivo, 'r') as f:
        return json.load(f)

def calcular_total_venta(venta):
    """Devuelve precio * cantidad para una venta."""
    return venta["precio"] * venta["cantidad"]

def ventas_por_categoria(ventas):
    """
    Agrupa las ventas por categoría.
    Devuelve un dict: { "categoria": total_euros }
    """
    totales = {}
    for venta in ventas:
        categoria = venta["categoria"]
        total = calcular_total_venta(venta)
        if categoria in totales:
            totales[categoria] += total
        else:
            totales[categoria] = total
    return totales

def producto_mas_vendido(ventas):
    """Devuelve el nombre del producto con mayor ingreso total."""
    productos = {}
    for venta in ventas:
        producto = venta["producto"]
        total = calcular_total_venta(venta)
        if producto in productos:
            productos[producto] += total
        else:
            productos[producto] = total
    return max(productos, key=productos.get)

def ventas_en_fecha(ventas, fecha_str):
    """Filtra ventas de una fecha específica (formato YYYY-MM-DD)."""
    fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
    return [venta for venta in ventas if datetime.strptime(venta["fecha"], "%Y-%m-%d") == fecha]

""" Paso 3: Generar el informe Implementa main() que imprima:"""

def main():
    ventas = cargar_ventas("ventas.json")
    
    print("Ventas por categoría:")
    totales_categoria = ventas_por_categoria(ventas)
    for categoria, total in totales_categoria.items():
        print(f"{categoria}: {total:.2f} euros")
    
    producto_top = producto_mas_vendido(ventas)
    print(f"\nProducto más vendido: {producto_top}")
    
    fecha_consulta = "18/05/2026"
    ventas_fecha = ventas_en_fecha(ventas, fecha_consulta)
    print(f"\nVentas en la fecha {fecha_consulta}:")
    for venta in ventas_fecha:
        print(venta)

""" Paso 4: Exportar resultados
Añade una función guardar_informe(informe, ruta) que guarde el informe en informe.json:"""
def guardar_informe(informe, ruta):
    """Guarda el informe en un archivo JSON."""
    with open(ruta, 'w') as f:
        json.dump(informe, f, indent=4)
        print(f"Informe guardado en {ruta}")