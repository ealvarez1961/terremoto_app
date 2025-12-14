import streamlit as st
import pandas as pd
import plotly.express as px
from quakefeeds import QuakeFeed
from datetime import datetime

##############################
### CONFIGURACIÓN DE PÁGINA
##############################
st.set_page_config(layout="wide")

##############################
### TÍTULO
##############################
st.markdown("""
<h1 style="
    text-align:center;
    font-size:32px;
    margin-bottom:5px;
">
    Datos en Tiempo Real de los Terremotos en Puerto Rico y el Mundo
</h1>
<hr style="margin-top:0; margin-bottom:20px;">
""", unsafe_allow_html=True)


##################################
### TOKEN MAPBOX
##################################
token_id = "pk.eyJ1IjoibWVjb2JpIiwiYSI6IjU4YzVlOGQ2YjEzYjE3NTcxOTExZTI2OWY3Y2Y1ZGYxIn0.LUg7xQhGH2uf3zA57szCyw"
px.set_mapbox_access_token(token_id)

#################################################
### FUNCIÓN PARA CLASIFICAR MAGNITUD (RICHTER)
#################################################
def clasificacion_richter(mag):
    if mag < 2:
        return "micro"
    elif 2 <= mag < 4:
        return "menor"
    elif 4 <= mag < 5:
        return "ligero"
    elif 5 <= mag < 6:
        return "moderado"
    elif 6 <= mag < 7:
        return "fuerte"
    elif 7 <= mag < 8:
        return "mayor"
    elif 8 <= mag < 10:
        return "épico"
    else:
        return "legendario"

##########################################
### BARRA LATERAL DE OPCIONES
##########################################

st.sidebar.markdown("<span style='color:red;'>Severidad</span>", unsafe_allow_html=True)
severidad = st.sidebar.selectbox("",
                                 ("todos", "significativo", "4.5", "2.5", "1.0"))

st.sidebar.markdown("<span style='color:red;'>Periodo</span>", unsafe_allow_html=True)
periodo = st.sidebar.selectbox("",
                               ("mes", "semana", "dia"))

st.sidebar.markdown("<span style='color:red;'>Zona Geográfica</span>", unsafe_allow_html=True)
zona_geografica = st.sidebar.selectbox("",
                                       ("Puerto Rico", "Mundo"))

st.sidebar.divider()
mapa = st.sidebar.checkbox("Mostrar mapa")
st.sidebar.divider()
tabla = st.sidebar.checkbox("Mostrar tabla con 5 eventos")

if tabla:
    ventana = st.sidebar.slider("Cantidad de Eventos", 5, 20)

st.sidebar.markdown("""Aplicacion desarrollada por :<br> <i> <u>Edgardo Alvarez</u> <br><br>
                    <b>INGE3016</b> <br>Universidad de Puerto Rico en Humacao</i>""",
                    unsafe_allow_html=True)  

st.sidebar.divider()


###############################
### CARGAR LOS DATOS
###############################
def generaTabla(severidad, periodo):

    periodo_dict = {"mes": "month", "semana": "week", "dia": "day"}
    periodo_api = periodo_dict[periodo]

    if severidad == "todos":
        th = "all"
    elif severidad == "significativo":
        th = "significant"
    else:
        th = severidad

    feed = QuakeFeed(th, periodo_api)

    longitudes = [feed.location(i)[0] for i in range(len(feed))]
    latitudes = [feed.location(i)[1] for i in range(len(feed))]
    fechas = list(feed.event_times)
    profundidades = list(feed.depths)
    lugares = list(feed.places)
    magnitudes = list(feed.magnitudes)

    df = pd.DataFrame({
        "fecha": fechas,
        "lon": longitudes,
        "lat": latitudes,
        "loc": lugares,
        "mag": magnitudes,
        "prof": profundidades
    })

    df = df.apply(pd.to_numeric, errors="ignore")
    df["clasificacion"] = df["mag"].apply(clasificacion_richter)

    # ========= FORMATO DE FECHA EN ESPAÑOL =========
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")

    meses_es = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
        5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
        9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }

    def formatea_fecha(f):
        if pd.isna(f):
            return ""
        return f"{f.day} de {meses_es[f.month]} de {f.year}"

    df["fecha"] = df["fecha"].apply(formatea_fecha)

    return df



df = generaTabla(severidad, periodo)

##########################################
### FILTRO POR ZONA GEOGRÁFICA
##########################################
if zona_geografica == "Puerto Rico":
    df = df[
        (df["lat"] >= 17.9) & (df["lat"] <= 18.5) &
        (df["lon"] >= -67.3) & (df["lon"] <= -65.5) ]
    
# evitar magnitudes negativas que dañan el mapa
df["mag"] = df["mag"].apply(lambda x: max(x, 0.1))

###############################################
### LIMPIEZA DE MAGNITUDES ANTES DEL MAPA
###############################################

# Reemplazar NaN por 0.1
df["mag"] = df["mag"].fillna(0.1)

# Reemplazar valores negativos por 0.1
df["mag"] = df["mag"].apply(lambda x: max(x, 0.1))

# Eliminar registros con lat/lon nulos (a veces vienen desde USGS)
df = df.dropna(subset=["lat", "lon"])

##########################################
### ESTADÍSTICAS SUPERIORES
##########################################
st.markdown(
    f"""
    <div style="text-align:center; font-size:16px;">
        <b>Fecha de petición:</b> {datetime.now().strftime("%Y-%m-%d %H:%M")}<br>
        <b>Cantidad de eventos:</b> {len(df)}<br>
        <b>Promedio de magnitudes:</b> {round(df["mag"].mean(), 3)}<br>
        <b>Promedio de profundidades:</b> {round(df["prof"].mean(), 3)}
    </div>
    """,
    unsafe_allow_html=True)

##########################################
### TABLA
##########################################
if tabla:
    st.write(df[["fecha", "loc", "mag", "clasificacion"]].head(ventana))

##########################################
### COLUMNAS
##########################################
col1, col2, col3 = st.columns([3,3,6])


##########################################
### MAPA
##########################################
def generaMapa(df, zona_geografica):
    if zona_geografica == "Puerto Rico":
        center = dict(lat=18.25178, lon=-66.254512)  # Centro en PR
        zoom = 7.5
    else:  # Mundo
        center = dict(lat=0, lon=0)  # Centro en el ecuador
        zoom = 1.0  # Zoom alejado para ver todo el planeta

    fig = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lon",
        color="mag",
        size="mag",
        hover_name="loc",
        hover_data={"mag": True,
                    "prof": True,
                    "lat": True,
                    "lon": True,
                    "fecha": True},
        color_continuous_scale=px.colors.cyclical.IceFire,
        size_max=10,
        opacity=0.5,
        center=center,
        width=2000,
        height=500, 
        mapbox_style="dark",
        zoom=zoom
    )

    return fig

if mapa:
    with col3:
        st.plotly_chart(generaMapa(df, zona_geografica), use_container_width=True)


##########################################
### HISTOGRAMAS
##########################################
def generaMag(df):
    fig = px.histogram(df, x="mag", title="Histograma de Magnitudes",
                       color_discrete_sequence=["red"], height=500)
    fig.update_layout(
        title_x=0.1,)
    
    return fig

with col1:
    st.plotly_chart(generaMag(df), use_container_width=True)

def generaProf(df):  
     fig = px.histogram(df, x="prof", title="Histograma de Profundidades",
                        color_discrete_sequence=["red"], height=500)
     fig.update_layout(
         title_x=0.02,)
       
     return fig

with col2:
    st.plotly_chart(generaProf(df), use_container_width=True)
