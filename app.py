# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Vehicles Dashboard", layout="wide")
st.header("🚗 Análisis de Datos de Vehículos 🚗")
st.write(
    "Bienvenido a esta aplicación web interactiva. 🕹️\n"
    "Aquí podrás visualizar datos relacionados con vehículos de manera sencilla y dinámica. 🏁"
)

# Carga de datos
car_data = pd.read_csv('vehicles_us.csv')

# Mostrar pequeñas muestras para verificar
st.subheader("Vista previa de los datos")
st.dataframe(car_data.head())


#Colorear gráficos por tipo de vehículo 
if 'type' in car_data.columns:
    color_col = 'type'
    st.info("🎨 Los gráficos se colorearán por tipo de vehículo")
else:
    color_col = None
    st.warning("⚠️ No se encontró la columna 'type'. Los gráficos no estarán coloreados.")

# --- Controles (botones + checkbox) ---
hist_button = st.button("Construir histograma 📉")
scatter_button = st.button("Construir gráfico de dispersión 📈")
build_bar = st.checkbox("Construir un gráfico de barras por tipo de vehículo 📊")

# Función helper para convertir a numérico de forma segura
def to_numeric_safe(series):
    return pd.to_numeric(series, errors="coerce")

# ---------- HISTOGRAMA ----------
if hist_button:
    st.write("Creando un histograma del kilometraje según el tipo de vehículo:")
    if "odometer" not in car_data.columns:
        st.warning("La columna 'odometer' no existe en el dataset.")
    else:
        df_hist = car_data.copy()
        df_hist["odometer"] = to_numeric_safe(df_hist["odometer"])
        df_hist = df_hist.dropna(subset=["odometer"])
        if df_hist.empty:
            st.warning("No hay valores numéricos válidos en 'odometer'.")
        else:
            try:
                if color_col:
                    fig_hist = px.histogram(
                        df_hist,
                        x="odometer",
                        color=color_col,
                        title="Distribución del kilometraje por tipo de vehículo",
                        color_discrete_sequence=px.colors.qualitative.Plotly
                    )
                else:
                    fig_hist = px.histogram(df_hist, x="odometer", title="Distribución del kilometraje")
                st.plotly_chart(fig_hist, use_container_width=True)
            except Exception as e:
                st.error(f"Error al crear el histograma: {e}")

# ---------- SCATTER ----------
if scatter_button:
    st.write("Creación de un gráfico de dispersión de odometer vs price")
    if ("odometer" not in car_data.columns) or ("price" not in car_data.columns):
        st.warning("Faltan las columnas 'odometer' y/o 'price' en el dataset.")
    else:
        df_sc = car_data.copy()
        df_sc["odometer"] = to_numeric_safe(df_sc["odometer"])
        df_sc["price"] = to_numeric_safe(df_sc["price"])
        df_sc = df_sc.dropna(subset=["odometer", "price"])
        if df_sc.empty:
            st.warning("No hay datos numéricos válidos para 'odometer' y 'price'.")
        else:
            try:
                if color_col:
                    fig_scatter = px.scatter(
                        df_sc,
                        x="odometer",
                        y="price",
                        color=color_col,
                        hover_data=[c for c in ("model_year", "model", "make") if c in df_sc.columns],
                        title="Precio vs Kilometraje por tipo de vehículo",
                        color_discrete_sequence=px.colors.qualitative.Plotly
                    )
                else:
                    fig_scatter = px.scatter(
                        df_sc,
                        x="odometer",
                        y="price",
                        hover_data=[c for c in ("model_year", "model", "make") if c in df_sc.columns],
                        title="Precio vs Kilometraje"
                    )
                st.plotly_chart(fig_scatter, use_container_width=True)
            except Exception as e:
                st.error(f"Error al crear el scatter: {e}")

# ---------- BARRAS ----------
if build_bar:
    st.write("Creación de un gráfico de barras que muestra la cantidad de vehículos por tipo")
    if color_col is None:
        st.warning("No hay columna 'type'/'make'/'model' para agrupar.")
    else:
        try:
            df_bar = car_data[color_col].fillna("Unknown").astype(str).value_counts().reset_index()
            df_bar.columns = [f"{color_col}_name", "count"]
            fig_bar = px.bar(
                df_bar,
                x=f"{color_col}_name",
                y="count",
                color=f"{color_col}_name",
                labels={f"{color_col}_name": "Tipo de vehículo", "count": "Cantidad"},
                title="Cantidad de vehículos por tipo",
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        except Exception as e:
            st.error(f"Error al crear el gráfico de barras: {e}")

# ---------- Footer (opcional) ----------
st.markdown("---")
st.caption("💡 Si algo no se ve bien, no te preocupes: a veces los datos necesitan un pequeño ajuste. ¡Gracias por explorar esta app! 🚗✨")