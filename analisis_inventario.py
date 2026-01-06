import pandas as pd
from sqlalchemy import create_engine
import numpy as np
from datetime import date

# --- 1. CONEXIÓN A LA BASE DE DATOS ---
# Usamos SQLAlchemy porque conecta mejor con Pandas
# Formato: mysql+mysqlconnector://usuario:password@host/nombre_bd
db_connection_str = 'mysql+mysqlconnector://root:@localhost/db_inventario_retail'
db_connection = create_engine(db_connection_str)

print("🔄 Conectando a MySQL y extrayendo datos crudos...")

# --- 2. EXTRACCIÓN (Extract) ---
# Traemos los datos a la memoria de Python
query_movimientos = "SELECT * FROM fact_movimientos"
query_productos = "SELECT * FROM dim_productos"

df_mov = pd.read_sql(query_movimientos, db_connection)
df_prod = pd.read_sql(query_productos, db_connection)

# --- 3. TRANSFORMACIÓN (Transform) ---

print("⚙️ Calculando Stock y Lógica FIFO...")
# A. CÁLCULO DE STOCK ACTUAL
# Si es ENTRADA suma, si es SALIDA resta
df_mov['cantidad_ajustada'] = df_mov.apply(
    lambda x: x['cantidad'] if x['tipo_movimiento'] == 'ENTRADA' else -x['cantidad'], axis=1
)

# Agrupamos por producto para tener el stock neto
df_stock = df_mov.groupby('id_producto')[
    'cantidad_ajustada'].sum().reset_index()
df_stock.rename(columns={'cantidad_ajustada': 'stock_actual'}, inplace=True)

print("📊 Realizando Clasificación ABC (Pareto)...")
# B. ANÁLISIS ABC (80/20)
# Filtramos solo lo que se vendió (SALIDAS)
df_ventas = df_mov[df_mov['tipo_movimiento'] == 'SALIDA'].copy()

# Cruzamos con la tabla de productos para saber el precio
df_ventas = df_ventas.merge(
    df_prod[['id_producto', 'precio_venta']], on='id_producto')
df_ventas['monto_venta'] = df_ventas['cantidad'] * df_ventas['precio_venta']

# Sumamos ventas por producto
df_abc = df_ventas.groupby('id_producto')['monto_venta'].sum().reset_index()
df_abc.sort_values('monto_venta', ascending=False, inplace=True)

# Calculamos % acumulado
df_abc['porcentaje_acumulado'] = df_abc['monto_venta'].cumsum() / \
    df_abc['monto_venta'].sum()

# Función para etiquetar A, B o C


def clasificar_abc(porcentaje):
    if porcentaje <= 0.80:
        return 'A'      # El 80% de tu dinero
    elif porcentaje <= 0.95:
        return 'B'    # El siguiente 15%
    else:
        return 'C'                       # El último 5% (relleno)


df_abc['clasificacion_abc'] = df_abc['porcentaje_acumulado'].apply(
    clasificar_abc)

print("⚠️ Detectando Riesgos de Vencimiento...")
# C. ANÁLISIS DE VENCIMIENTO
# Filtramos entradas que tienen fecha de vencimiento
df_venc = df_mov[(df_mov['tipo_movimiento'] == 'ENTRADA') &
                 (df_mov['fecha_vencimiento'].notnull())].copy()

# Convertimos a formato fecha
df_venc['fecha_vencimiento'] = pd.to_datetime(df_venc['fecha_vencimiento'])
hoy = pd.to_datetime(date.today())

# Calculamos días restantes
df_venc['dias_para_vencer'] = (df_venc['fecha_vencimiento'] - hoy).dt.days

# Nos quedamos con la fecha más peligrosa (mínima) por producto
df_riesgo = df_venc.groupby('id_producto')[
    'dias_para_vencer'].min().reset_index()


def definir_alerta(dias):
    if dias < 0:
        return 'VENCIDO'
    elif dias <= 30:
        return 'CRÍTICO'
    elif dias <= 60:
        return 'PRECAUCIÓN'
    else:
        return 'OK'


df_riesgo['estado_vencimiento'] = df_riesgo['dias_para_vencer'].apply(
    definir_alerta)

# --- 4. CARGA (Load) ---
# Unimos todas las tablas calculadas en una sola
df_final = df_prod.merge(df_stock, on='id_producto', how='left')
df_final = df_final.merge(
    df_abc[['id_producto', 'clasificacion_abc', 'monto_venta']], on='id_producto', how='left')
df_final = df_final.merge(df_riesgo, on='id_producto', how='left')

# Limpiamos nulos (NaN) poniendo ceros o textos
df_final['stock_actual'] = df_final['stock_actual'].fillna(0)
df_final['clasificacion_abc'] = df_final['clasificacion_abc'].fillna('C')
df_final['estado_vencimiento'] = df_final['estado_vencimiento'].fillna(
    'SIN FECHA')

print("💾 Guardando tabla maestra 'reporte_bi_final' en MySQL...")

# Esto crea la tabla lista para Power BI
df_final.to_sql('reporte_bi_final', db_connection,
                if_exists='replace', index=False)

print("✅ ¡Proceso ETL Terminado Exitosamente!")
