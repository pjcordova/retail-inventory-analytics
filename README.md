# 🛒 Retail Inventory Intelligence: End-to-End Analytics

![Power BI](https://img.shields.io/badge/Business%20Intelligence-Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Python](https://img.shields.io/badge/Data%20Gen-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/Storage-MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Status](https://img.shields.io/badge/Status-Finalizado-success?style=for-the-badge)

## 📋 Descripción Ejecutiva
Este proyecto es una solución integral de **Inteligencia de Negocios (BI)** para el sector Retail. Simula, procesa y visualiza el inventario de un supermercado para optimizar la cadena de suministro.

El sistema aborda dos problemas críticos de negocio:
1.  **Control de Mermas:** Reducción de pérdidas por vencimiento de productos perecederos.
2.  **Optimización de Stock:** Segmentación de productos (Pareto ABC) para estrategias de venta inteligentes.

---

## 🏗️ Arquitectura del Pipeline (End-to-End)

El proyecto no es solo un dashboard; es un flujo de datos completo **ETL (Extract, Transform, Load)**:

```mermaid
graph LR
    A[("Generador Python (Faker)")] -->|Datos Sintéticos| B(MySQL / Data Warehouse)
    B -->|SQL Queries| C{Power BI Data Model}
    C -->|DAX| D[Cálculo de Semáforos]
    D -->|Visualización| E[Dashboard Gerencial]
