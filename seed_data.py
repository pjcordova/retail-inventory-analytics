import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta

# --- CONFIGURACIÓN ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Déjalo vacío si no usas contraseña
    'database': 'db_inventario_retail'
}

fake = Faker('es_ES')

CATEGORIAS = {1: 'Lácteos', 2: 'Abarrotes', 3: 'Bebidas', 4: 'Limpieza'}

PRODUCTOS_BASE = {
    1: [('Leche Gloria', 4.5, 5.2), ('Yogurt Laive', 6.0, 8.5), ('Mantequilla', 8.0, 10.5)],
    2: [('Arroz Costeño', 18.0, 24.0), ('Azúcar Rubia', 3.5, 4.8), ('Fideos Don Vittorio', 2.5, 3.8)],
    3: [('Coca Cola 3L', 9.0, 12.5), ('Agua San Mateo', 2.0, 3.0), ('Cerveza Pack', 20.0, 35.0)],
    4: [('Detergente Bolivar', 15.0, 22.0), ('Lejía Sapolio', 4.0, 6.0)]
}


def conectar_bd():
    return mysql.connector.connect(**DB_CONFIG)


def limpiar_tablas(cursor):
    print("🧹 Limpiando datos antiguos...")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    cursor.execute("TRUNCATE TABLE fact_movimientos")
    cursor.execute("TRUNCATE TABLE dim_productos")
    cursor.execute("TRUNCATE TABLE dim_categorias")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")


def generar_data():
    conn = conectar_bd()
    cursor = conn.cursor()
    limpiar_tablas(cursor)

    print("🚀 Insertando Categorías y Productos...")
    # CORRECCIÓN AQUÍ: Agregamos nombres de columnas explícitos
    for id_cat, nombre in CATEGORIAS.items():
        cursor.execute(
            "INSERT INTO dim_categorias (id_categoria, nombre_categoria) VALUES (%s, %s)", (id_cat, nombre))

    ids_productos = []
    for _ in range(50):
        cat_id = random.choice(list(CATEGORIAS.keys()))
        prod_base = random.choice(PRODUCTOS_BASE[cat_id])
        nombre = f"{prod_base[0]} {fake.word().capitalize()}"
        sku = f"PROD-{fake.unique.random_number(digits=5)}"
        ids_productos.append(sku)

        # CORRECCIÓN AQUÍ: Agregamos nombres de columnas explícitos
        sql_prod = """INSERT INTO dim_productos (id_producto, nombre, id_categoria, precio_costo, precio_venta) 
                      VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql_prod, (sku, nombre, cat_id,
                       prod_base[1], prod_base[2]))

    # --- INVENTARIO INICIAL (SALUDABLE) ---
    print("🚚 Cargando Inventario Inicial Sano...")
    hoy = datetime.now()
    for sku in ids_productos:
        fecha_venc = hoy + timedelta(days=random.randint(200, 400))
        # CORRECCIÓN AQUÍ: Agregamos nombres de columnas explícitos
        sql_ini = """INSERT INTO fact_movimientos 
                     (id_producto, tipo_movimiento, cantidad, fecha_movimiento, lote_codigo, fecha_vencimiento) 
                     VALUES (%s, 'ENTRADA', 100, %s, 'INI-001', %s)"""
        cursor.execute(
            sql_ini, (sku, (hoy - timedelta(days=100)).date(), fecha_venc.date()))

    # --- MOVIMIENTOS CONTROLADOS ---
    print("🔄 Generando Movimientos 'Portafolio Friendly'...")
    for _ in range(600):
        sku = random.choice(ids_productos)
        tipo = random.choices(['ENTRADA', 'SALIDA'], weights=[0.4, 0.6])[0]

        dias_random = random.randint(0, 90)
        fecha_mov = hoy - timedelta(days=90) + timedelta(days=dias_random)

        fecha_venc = None
        if tipo == 'ENTRADA':
            # --- TRUCO: 90% de probabilidad de ser VERDE (OK) ---
            escenario = random.choices(
                ['CRITICO', 'ALERTA', 'OK'], weights=[0.05, 0.05, 0.90])[0]

            if escenario == 'CRITICO':
                dias_extra = random.randint(1, 29)  # Rojo
            elif escenario == 'ALERTA':
                dias_extra = random.randint(31, 59)  # Amarillo
            else:
                dias_extra = random.randint(65, 300)  # Verde

            fecha_venc = hoy + timedelta(days=dias_extra)

        sql_mov = """INSERT INTO fact_movimientos 
                     (id_producto, tipo_movimiento, cantidad, fecha_movimiento, lote_codigo, fecha_vencimiento) 
                     VALUES (%s, %s, %s, %s, %s, %s)"""

        cursor.execute(sql_mov, (sku, tipo, random.randint(5, 20), fecha_mov.date(), 'LOTE-X',
                                 None if tipo == 'SALIDA' else fecha_venc.date()))

    conn.commit()
    conn.close()
    print("✅ ¡Datos listos! Ahora ejecuta analisis_inventario.py")


if __name__ == "__main__":
    generar_data()
