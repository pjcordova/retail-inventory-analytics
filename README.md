# 🛒 Retail Inventory Intelligence: Power BI & SQL Analytics

![Power BI](https://img.shields.io/badge/Business%20Intelligence-Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![DAX](https://img.shields.io/badge/Language-DAX-00758F?style=for-the-badge&logo=powerbi&logoColor=white)
![SQL](https://img.shields.io/badge/Data-SQL-CC2927?style=for-the-badge&logo=microsoftsqlserver&logoColor=white)
![Status](https://img.shields.io/badge/Status-Finalizado-success?style=for-the-badge)

## 📋 Descripción Ejecutiva
Este proyecto consiste en una solución de **Inteligencia de Negocios (BI)** diseñada para optimizar la cadena de suministro de una empresa de Retail.

El objetivo principal es reducir las pérdidas por "Out-of-Stock" (quiebres de stock) y optimizar la rotación de inventarios mediante un dashboard interactivo que permite a los gerentes de logística tomar decisiones basadas en datos en tiempo real.

---

## 🏗️ Flujo de Datos (Data Pipeline)

El proceso sigue el estándar de la industria para BI (ETL + Modelado + Visualización):

```mermaid
graph LR
    A[("Fuente de Datos (SQL/Excel)")] --> B(Power Query ETL)
    B -- Limpieza & Transformación --> C{Modelo de Datos}
    C -- Star Schema --> D[Cálculos DAX]
    D --> E[Dashboard Interactivo]
    E --> F[Toma de Decisiones]
