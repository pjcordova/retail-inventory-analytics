    # Desarrollo de Pipeline de Datos End-to-End para Analítica de Inventarios

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-Desktop-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Status](https://img.shields.io/badge/Status-Completado-success?style=for-the-badge)

## 📋 Descripción del Proyecto

Este proyecto consiste en el desarrollo de una solución integral de **Inteligencia de Negocios (BI)** para el sector Retail. El objetivo principal fue construir un pipeline de datos que permita simular, procesar y visualizar el inventario de un supermercado para optimizar la toma de decisiones logísticas.

El sistema aborda problemas críticos de negocio como el **control de mermas** (pérdidas por vencimiento) y la **segmentación de productos** para estrategias de venta.

## 🚀 Arquitectura y Flujo de Datos

El proyecto sigue un flujo **ETL (Extract, Transform, Load)** automatizado:

1.  **Ingesta & Generación (Python + Faker):**
    * Script en Python que genera datos transaccionales sintéticos realistas.
    * Simulación de miles de movimientos (entradas y salidas) con fechas históricas y futuras.
2.  **Almacenamiento (MySQL):**
    * Diseño de un **Data Warehouse** relacional (Esquema Estrella).
    * Tablas dimensionales (`dim_productos`, `dim_categorias`) y tabla de hechos (`fact_movimientos`).
3.  **Procesamiento & Lógica de Negocio (Python):**
    * Implementación de algoritmos para cálculo de **Stock Actual** y **Días para Vencer**.
    * Clasificación automática de alertas: `CRÍTICO`, `PRECAUCIÓN`, `OK`.
4.  **Visualización (Power BI):**
    * Conexión directa a base de datos.
    * Dashboard interactivo con análisis de Pareto (ABC) y valoración financiera del riesgo.

## 📊 Visualización del Dashboard

![Vista Previa del Dashboard](dashboard_preview.png)
*(El dashboard permite filtrar por estado de vencimiento y visualizar el impacto económico de los productos en riesgo)*

## 🛠️ Tecnologías y Herramientas

* **Lenguaje:** Python (Librerías: `pandas`, `faker`, `mysql-connector`).
* **Base de Datos:** MySQL Server 8.0.
* **Visualización:** Microsoft Power BI.
* **IDE:** Visual Studio Code.

## 🧠 Lógica de Negocio Implementada

### 1. Semáforo de Riesgo (Gestión de Mermas)
Se implementó un sistema de alertas basado en la proximidad de la fecha de caducidad:
* 🔴 **CRÍTICO:** Vence en menos de 30 días (Acción: Liquidación inmediata).
* 🟡 **PRECAUCIÓN:** Vence entre 30 y 60 días (Acción: Ofertas promocionales).
* 🟢 **OK:** Vence en más de 60 días (Stock saludable).

### 2. Clasificación ABC (Pareto)
Análisis de la distribución de ventas para identificar productos clave:
* **Categoría A:** El 20% de los productos que generan el 80% de los ingresos.
* **Categoría B y C:** Productos de rotación media y baja.

## 📂 Estructura del Repositorio

```text
├── seed_data.py            # Script para generación de datos sintéticos y carga a MySQL
├── analisis_inventario.py  # Script ETL para lógica de negocio y creación de tabla de reporte
├── db_schema.sql           # Estructura de la base de datos (DDL)
├── dashboard_retail.pbix   # Archivo fuente de Power BI
├── requirements.txt        # Dependencias de Python
└── README.md               # Documentación del proyecto