# ============================================================
# Diabetes Health Indicators — BRFSS 2015
# Herramientas y Visualización de Datos — Proyecto 2
# Streamlit App | Python
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="Diabetes Health Indicators — BRFSS 2015",
    page_icon="🩺",
    layout="wide"
)

st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; padding-bottom: 1rem; }
    [data-testid="stSidebar"] { background-color: #f8f9fa; }
    .titulo { border-bottom: 3px solid #E41A1C; padding-bottom: 12px; margin-bottom: 20px; }
    .titulo h1 { font-size: 20px; font-weight: 700; color: #1a1a2e; margin: 0 0 4px; }
    .titulo p  { font-size: 12px; color: #6c757d; margin: 0; }
    .insight { background: #fffbeb; border-left: 4px solid #f6ad55; padding: 9px 13px;
               border-radius: 0 6px 6px 0; margin-bottom: 12px; font-size: 13px; color: #3d3d3d; }
    .ctitle { font-size: 14px; font-weight: 700; color: #1a1a2e; margin-bottom: 2px; }
    .csub   { font-size: 12px; color: #718096; margin-bottom: 8px; }
    .fuente { font-size: 11px; color: #adb5bd; text-align: right; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

COLOR  = {"Sin Diabetes": "#4DAF4A", "Prediabetes": "#FF7F00", "Diabetes": "#E41A1C"}
GRUPOS = ["Sin Diabetes", "Prediabetes", "Diabetes"]

@st.cache_data
def cargar_datos():
    df = pd.read_csv("data/diabetes_012_health_indicators_BRFSS2015.csv")
    df["Diabetes_Label"] = df["Diabetes_012"].map({0:"Sin Diabetes",1:"Prediabetes",2:"Diabetes"})
    return df

df_raw = cargar_datos()

st.markdown("""
<div class="titulo">
    <h1>Indicadores de Salud y Riesgo de Diabetes — EE.UU. 2015</h1>
    <p>Behavioral Risk Factor Surveillance System (BRFSS) · CDC · n = 253,680 · 22 variables</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Filtros")
    st.markdown("**Condición diabética**")
    sel_grupos = []
    for g in GRUPOS:
        if st.checkbox(g, value=True, key=f"cb_{g}"):
            sel_grupos.append(g)
    st.markdown("---")
    st.caption("Los filtros aplican a todas las visualizaciones excepto el mapa de correlaciones.")

df = df_raw[df_raw["Diabetes_Label"].isin(sel_grupos)] if sel_grupos else df_raw.head(0)

def layout(h=400, yrange=None, ytitle="", xtitle="", barmode=None, bargap=0.3, bargroupgap=0.05, tickformat=None):
    l = dict(
        height=h,
        margin=dict(l=60, r=20, t=10, b=50),
        plot_bgcolor="white", paper_bgcolor="white",
        font=dict(family="Helvetica Neue, Helvetica, Arial, sans-serif", size=12, color="#2d2d2d"),
        xaxis=dict(showgrid=False, linecolor="#e2e8f0", title=xtitle),
        yaxis=dict(gridcolor="#e2e8f0", title=ytitle, range=yrange, tickformat=tickformat),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
                    bgcolor="rgba(0,0,0,0)"),
        bargap=bargap, bargroupgap=bargroupgap
    )
    if barmode: l["barmode"] = barmode
    return l

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Comparación por grupo", "Distribución de BMI",
    "Factores de riesgo", "Prevalencia por edad", "Mapa de correlaciones"
])

with tab1:
    st.markdown('<div class="insight"><b>Hallazgo:</b> El 84.2% de los encuestados no reporta diabetes. La prediabetes representa solo el 1.8%, lo que sugiere un alto nivel de subdiagnóstico en la población general.</div>', unsafe_allow_html=True)
    st.markdown('<div class="ctitle">Distribución de encuestados según condición diabética</div>', unsafe_allow_html=True)
    st.markdown('<div class="csub">Conteo absoluto y porcentaje sobre el total filtrado</div>', unsafe_allow_html=True)
    if df.empty:
        st.warning("Selecciona al menos un grupo.")
    else:
        conteos = df["Diabetes_Label"].value_counts().reindex([g for g in GRUPOS if g in sel_grupos]).dropna()
        total   = conteos.sum()
        pcts    = (conteos / total * 100).round(1)
        fig = go.Figure()
        for g in conteos.index:
            fig.add_trace(go.Bar(
                x=[g], y=[conteos[g]], marker_color=COLOR[g], showlegend=False,
                text=f"{conteos[g]:,.0f}<br>({pcts[g]}%)",
                textposition="outside", textfont=dict(size=12, color="#2d2d2d")
            ))
        fig.update_layout(**layout(ytitle="Número de personas", tickformat=",", bargap=0.45))
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="fuente">Fuente: CDC BRFSS 2015 — Kaggle</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="insight"><b>Hallazgo:</b> La mediana del IMC en personas con diabetes (~31) es notablemente mayor que en personas sin diabetes (~27). El sobrepeso y la obesidad son factores de riesgo centrales.</div>', unsafe_allow_html=True)
    st.markdown('<div class="ctitle">Distribución del IMC (BMI) según condición diabética</div>', unsafe_allow_html=True)
    st.markdown('<div class="csub">Cajas: Q1–Q3 · Línea: mediana · Punto: media · Bigotes: 1.5×IQR</div>', unsafe_allow_html=True)
    if df.empty:
        st.warning("Selecciona al menos un grupo.")
    else:
        fig = go.Figure()
        for g in [gr for gr in GRUPOS if gr in sel_grupos]:
            vals = df[df["Diabetes_Label"] == g]["BMI"].dropna().values
            fig.add_trace(go.Box(
                y=vals, name=g, marker_color=COLOR[g], fillcolor=COLOR[g],
                opacity=0.85, line=dict(color="#1a1a2e", width=1.5),
                boxmean="sd", showlegend=False, boxpoints=False
            ))
        fig.update_layout(**layout(ytitle="Índice de Masa Corporal (BMI)", yrange=[10,70]))
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="fuente">Fuente: CDC BRFSS 2015 — Kaggle</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="insight"><b>Hallazgo:</b> La hipertensión (75.3%) y el colesterol alto (67%) son los factores de riesgo más prevalentes en personas con diabetes. La actividad física es notablemente menor en ese grupo.</div>', unsafe_allow_html=True)
    st.markdown('<div class="ctitle">Prevalencia de factores de riesgo por condición diabética</div>', unsafe_allow_html=True)
    st.markdown('<div class="csub">Porcentaje de personas con cada factor de riesgo presente</div>', unsafe_allow_html=True)
    if df.empty:
        st.warning("Selecciona al menos un grupo.")
    else:
        fcols   = ["HighBP","HighChol","Smoker","PhysActivity","HeartDiseaseorAttack"]
        flabels = ["Hipertensión","Col. alto","Fumador","Act. física","Enf. cardíaca"]
        fig = go.Figure()
        for g in [gr for gr in GRUPOS if gr in sel_grupos]:
            sub  = df[df["Diabetes_Label"] == g]
            vals = [round(sub[c].mean()*100, 1) for c in fcols]
            fig.add_trace(go.Bar(
                name=g, x=flabels, y=vals, marker_color=COLOR[g],
                text=[f"{v}%" for v in vals], textposition="outside", textfont=dict(size=10)
            ))
        fig.update_layout(**layout(ytitle="Proporción (%)", yrange=[0,105],
                                    barmode="group", bargap=0.2, bargroupgap=0.05))
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="fuente">Fuente: CDC BRFSS 2015 — Kaggle</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="insight"><b>Hallazgo:</b> La prevalencia de diabetes aumenta sostenidamente con la edad. En el grupo 60–64 años supera el 25% de los encuestados, y sigue creciendo en los grupos mayores.</div>', unsafe_allow_html=True)
    st.markdown('<div class="ctitle">Composición de la condición diabética según grupo de edad</div>', unsafe_allow_html=True)
    st.markdown('<div class="csub">Barras apiladas al 100% — cada barra representa un grupo etario</div>', unsafe_allow_html=True)
    if df.empty:
        st.warning("Selecciona al menos un grupo.")
    else:
        elabels = {1:"18-24",2:"25-29",3:"30-34",4:"35-39",5:"40-44",6:"45-49",
                   7:"50-54",8:"55-59",9:"60-64",10:"65-69",11:"70-74",12:"75-79",13:"80+"}
        gord = [g for g in GRUPOS if g in sel_grupos]
        de   = df_raw[df_raw["Diabetes_Label"].isin(gord)].copy()
        de["GrupoEdad"] = de["Age"].map(elabels)
        pivot = de.groupby(["GrupoEdad","Diabetes_Label"]).size().unstack(fill_value=0)
        pivot = pivot.reindex(columns=gord, fill_value=0)
        ppct  = pivot.div(pivot.sum(axis=1), axis=0)*100
        ppct  = ppct.reindex([elabels[i] for i in range(1,14)])
        fig = go.Figure()
        for g in gord:
            fig.add_trace(go.Bar(
                name=g, x=ppct.index.tolist(), y=ppct[g].round(1).tolist(),
                marker_color=COLOR[g],
                hovertemplate="%{x}<br>"+g+": %{y:.1f}%<extra></extra>"
            ))
        fig.update_layout(**layout(ytitle="Proporción (%)", xtitle="Grupo de edad (años)",
                                    yrange=[0,102], barmode="stack", bargap=0.15))
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="fuente">Fuente: CDC BRFSS 2015 — Kaggle</div>', unsafe_allow_html=True)

with tab5:
    st.markdown('<div class="insight"><b>Hallazgo:</b> Diabetes correlaciona principalmente con salud general percibida (0.30), hipertensión (0.27) y BMI (0.22). La actividad física muestra correlación negativa consistente (−0.12).</div>', unsafe_allow_html=True)
    st.markdown('<div class="ctitle">Matriz de correlación de Pearson entre indicadores de salud</div>', unsafe_allow_html=True)
    st.markdown('<div class="csub">Paleta divergente: rojo = correlación positiva · azul = correlación negativa</div>', unsafe_allow_html=True)
    vcols = ["Diabetes_012","HighBP","HighChol","BMI","Smoker","PhysActivity","GenHlth","Age","Income"]
    vlabs = ["Diabetes","Hipertensión","Col. alto","BMI","Fumador","Act. física","Salud gral.","Edad","Ingreso"]
    mat = df_raw[vcols].corr().round(3)
    mat.columns = vlabs; mat.index = vlabs
    z    = mat.values.tolist()
    text = [[f"{v:.2f}" for v in row] for row in mat.values]
    fig = go.Figure(go.Heatmap(
        z=z, x=vlabs, y=vlabs,
        text=text, texttemplate="%{text}",
        colorscale="RdBu_r", zmin=-1, zmax=1, zmid=0,
        colorbar=dict(title="Pearson r", thickness=14)
    ))
    fig.update_layout(
        height=480, margin=dict(l=100, r=20, t=10, b=120),
        plot_bgcolor="white", paper_bgcolor="white",
        font=dict(family="Helvetica Neue, Helvetica, Arial, sans-serif", size=11),
        xaxis=dict(tickangle=-40, side="bottom"),
        yaxis=dict(autorange="reversed")
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="fuente">Fuente: CDC BRFSS 2015 — Kaggle</div>', unsafe_allow_html=True)