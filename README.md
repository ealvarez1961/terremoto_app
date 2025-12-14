# 🎈 Blank app template

A simple Streamlit app template for you to modify!

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```
# Visualización de Terremotos en Tiempo Real

Aplicación desarrollada en **Python** utilizando **Streamlit**, **Plotly** y datos sísmicos obtenidos mediante la librería `quakefeeds`.

## Descripción
Esta aplicación permite visualizar terremotos ocurridos recientemente en:
- Puerto Rico
- Todo el mundo

El usuario puede filtrar por:
- Severidad del evento
- Periodo de tiempo (día, semana, mes)
- Zona geográfica

Incluye:
- Mapa interactivo
- Histogramas de magnitudes y profundidades
- Tabla de eventos sísmicos

## Tecnologías utilizadas
- Python
- Streamlit
- Pandas
- Plotly
- QuakeFeeds
- Mapbox

## Cómo ejecutar la aplicación

1. Instalar dependencias:
```bash
pip install streamlit pandas plotly quakefeeds
