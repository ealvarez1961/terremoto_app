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
## Correr el app
   $ streamlit run streamlit_app.py