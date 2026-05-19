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

    total_ventas = len(ventas)
    ingresos_totales = sum(calcular_total_venta(v) for v in ventas)

    # Totales por categoría
    totales_categoria = ventas_por_categoria(ventas)

    # Producto más rentable
    producto_top = producto_mas_vendido(ventas)
    ingreso_top = sum(
        calcular_total_venta(v) for v in ventas if v["producto"] == producto_top
    )

    # Ventas en fecha específica
    fecha_consulta = "2026-01-16"
    ventas_fecha = ventas_en_fecha(ventas, fecha_consulta)

    # --- IMPRESIÓN DEL INFORME ---
    print("============================")
    print("     INFORME DE VENTAS")
    print("============================\n")

    print(f"Total de ventas: {total_ventas}")
    print(f"Ingresos totales: {ingresos_totales:,.2f} €\n".replace(",", "X").replace(".", ",").replace("X", "."))

    print("--- Por categoría ---")
    for categoria, total in totales_categoria.items():
        print(f"{categoria:<12}: {total:,.2f} €".replace(",", "X").replace(".", ",").replace("X", "."))

    print(f"\nProducto más rentable: {producto_top} ({ingreso_top:,.2f} €)".replace(",", "X").replace(".", ",").replace("X", "."))

    print(f"\n--- Ventas del {fecha_consulta} ---")
    for venta in ventas_fecha:
        total = calcular_total_venta(venta)
        print(f"- {venta['producto']}: {total:,.2f} €".replace(",", "X").replace(".", ",").replace("X", "."))

    informe = {
        "generado_en": datetime.now().isoformat(),
        "total_ventas": total_ventas,
        "ingresos_totales": round(ingresos_totales, 2),
        "por_categoria": {k: round(v, 2) for k, v in totales_categoria.items()},
        "producto_top": producto_top
    }

    guardar_informe(informe, "informe.json")


""" Paso 4: Exportar resultados
Añade una función guardar_informe(informe, ruta) que guarde el informe en informe.json:"""
def guardar_informe(informe, ruta):
    """Guarda el informe en un archivo JSON."""
    with open(ruta, 'w') as f:
        json.dump(informe, f, indent=4)
        print(f"Informe guardado en {ruta}")