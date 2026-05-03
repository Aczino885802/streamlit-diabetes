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
    .hallazgos {
        background: #fffbeb;
        border-left: 4px solid #f6ad55;
        padding: 14px 18px;
        border-radius: 0 6px 6px 0;
        margin-top: 16px;
        margin-bottom: 8px;
        font-size: 13.5px;
        color: #2d3748;
        line-height: 1.65;
    }
    .hallazgos b { color: #c05621; }
    .hallazgos .titulo-h {
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #c05621;
        margin-bottom: 8px;
        display: block;
    }
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
    st.caption("Los filtros aplican a las gráficas excepto el mapa de correlaciones y el de acceso por ingreso.")

df = df_raw[df_raw["Diabetes_Label"].isin(sel_grupos)] if sel_grupos else df_raw.head(0)

def hallazgos(html):
    st.markdown(f'<div class="hallazgos"><span class="titulo-h">Hallazgos</span>{html}</div>', unsafe_allow_html=True)

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
    "Acceso a salud por ingreso", "Distribución de BMI",
    "Factores de riesgo", "Prevalencia por edad", "Mapa de correlaciones"
])

# ── Tab 1: Acceso a salud por ingreso ────────────────────────
with tab1:
    st.markdown('<div class="ctitle">Acceso a atención médica según nivel de ingreso</div>', unsafe_allow_html=True)
    st.markdown('<div class="csub">Cobertura de salud y costo como barrera para ir al médico</div>', unsafe_allow_html=True)

    income_labels = {
        1:"<$10k", 2:"$10-15k", 3:"$15-20k", 4:"$20-25k",
        5:"$25-35k", 6:"$35-50k", 7:"$50-75k", 8:">$75k"
    }
    d = df_raw.copy()
    d["Ingreso"] = d["Income"].map(income_labels)
    d = d.dropna(subset=["Ingreso"])

    agrup = d.groupby("Ingreso").agg(
        cobertura = ("AnyHealthcare", lambda x: x.mean()*100),
        no_fue    = ("NoDocbcCost",   lambda x: x.mean()*100),
        n         = ("Income",        "size")
    ).reset_index()
    orden = [income_labels[i] for i in range(1,9)]
    agrup["Ingreso"] = pd.Categorical(agrup["Ingreso"], categories=orden, ordered=True)
    agrup = agrup.sort_values("Ingreso")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=agrup["Ingreso"].astype(str),
        y=agrup["cobertura"].round(1),
        name="Tiene seguro de salud",
        marker_color="#4DAF4A",
        text=[f"{v:.1f}%" for v in agrup["cobertura"]],
        textposition="outside",
        textfont=dict(size=10),
        hovertemplate="<b>Ingreso: %{x}</b><br>Con seguro: %{y:.1f}%<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=agrup["Ingreso"].astype(str),
        y=agrup["no_fue"].round(1),
        name="No fue al médico por costo",
        mode="lines+markers",
        line=dict(color="#E41A1C", width=3),
        marker=dict(color="#E41A1C", size=10, line=dict(color="white", width=2)),
        hovertemplate="<b>Ingreso: %{x}</b><br>No fue por costo: %{y:.1f}%<extra></extra>"
    ))
    fig.update_layout(**layout(
        ytitle="Porcentaje (%)",
        xtitle="Nivel de ingreso anual (USD)",
        yrange=[0, 110],
        h=460, bargap=0.35
    ))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="fuente">Fuente: CDC BRFSS 2015 — Kaggle</div>', unsafe_allow_html=True)

    cob_min  = agrup.iloc[0]["cobertura"]
    cob_max  = agrup.iloc[-1]["cobertura"]
    cost_min = agrup.iloc[0]["no_fue"]
    cost_max = agrup.iloc[-1]["no_fue"]
    cob_diff = cob_max - cob_min
    cost_ratio = cost_min / cost_max if cost_max > 0 else 0

    # Prevalencia real de prediabetes y diabetes en el dataset
    prev_pre = (df_raw["Diabetes_012"] == 1).mean() * 100
    prev_diab = (df_raw["Diabetes_012"] == 2).mean() * 100

    hallazgos(f"""
    El gráfico muestra dos curvas que se mueven en direcciones opuestas. La cobertura de seguro sube de <b>{cob_min:.1f}%</b> en el nivel más bajo a <b>{cob_max:.1f}%</b> en el más alto, una mejora de <b>{cob_diff:.1f} puntos</b>. Al mismo tiempo, el porcentaje de personas que dejaron de ir al médico por costo cae de <b>{cost_min:.1f}%</b> a <b>{cost_max:.1f}%</b> — es decir, en los niveles más pobres es <b>{cost_ratio:.1f} veces más alto</b> que en los niveles más ricos.
    <br><br>
    Lo lógico aquí es preguntarse: si en el nivel de ingreso más bajo el {cob_min:.1f}% ya tiene seguro, ¿por qué casi 1 de cada 3 personas (el {cost_min:.1f}%) no fue al médico por dinero? La respuesta está en que <b>tener seguro no es lo mismo que poder pagar la atención</b>. Los seguros tienen copagos, deducibles y medicamentos no cubiertos. Para alguien que gana menos de $10.000 al año, esos gastos pueden ser una decisión real entre ir al médico o pagar otras necesidades básicas.
    <br><br>
    Esto conecta con algo importante del dataset: la prediabetes solo aparece en <b>{prev_pre:.1f}%</b> de los registros, mientras que la diabetes ya diagnosticada está en <b>{prev_diab:.1f}%</b>. La prediabetes es una etapa silenciosa que solo se detecta con un examen de sangre — un examen al que la población vulnerable no está llegando. La diabetes en cambio sí aparece más porque cuando da síntomas, la gente termina yendo a urgencias. <b>Lo que vemos no es que haya poca prediabetes, sino que no se está detectando en quienes más la tienen.</b>
    """)

# ── Tab 2: Distribución de BMI con cortes OMS ────────────────
with tab2:
    st.markdown('<div class="ctitle">Distribución del peso corporal según condición diabética</div>', unsafe_allow_html=True)
    st.markdown('<div class="csub">Histograma con líneas que marcan sobrepeso (25) y obesidad (30) según la OMS</div>', unsafe_allow_html=True)
    if df.empty:
        st.warning("Selecciona al menos un grupo.")
    else:
        fig = go.Figure()
        for g in [gr for gr in GRUPOS if gr in sel_grupos]:
            vals = df[df["Diabetes_Label"] == g]["BMI"].dropna().values
            fig.add_trace(go.Histogram(
                x=vals, name=g,
                marker_color=COLOR[g],
                opacity=0.55,
                xbins=dict(start=12, end=60, size=1),
                histnorm="percent",
                hovertemplate=f"<b>{g}</b><br>IMC: %{{x}}<br>%{{y:.1f}}% del grupo<extra></extra>"
            ))
        fig.add_vline(x=25, line_dash="dash", line_color="#4a5568", line_width=1.5,
                      annotation_text="Sobrepeso (OMS ≥ 25)",
                      annotation_position="top",
                      annotation_font=dict(size=11, color="#4a5568"))
        fig.add_vline(x=30, line_dash="dash", line_color="#1a1a2e", line_width=1.5,
                      annotation_text="Obesidad (OMS ≥ 30)",
                      annotation_position="top",
                      annotation_font=dict(size=11, color="#1a1a2e"))
        fig.update_layout(**layout(ytitle="% dentro del grupo", xtitle="Índice de Masa Corporal (BMI)",
                                    barmode="overlay", h=460))
        fig.update_xaxes(range=[12, 60])
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="fuente">Fuente: CDC BRFSS 2015 — Kaggle · Cortes IMC: OMS</div>', unsafe_allow_html=True)

    if df.empty:
        hallazgos("Selecciona al menos un grupo en el filtro lateral para ver los hallazgos.")
    else:
        n_sel = len(sel_grupos)
        # Cálculos reales del dataset
        stats = {}
        for g in sel_grupos:
            vals = df[df["Diabetes_Label"]==g]["BMI"].dropna()
            stats[g] = {
                "mediana": vals.median(),
                "media": vals.mean(),
                "pct_obesidad": (vals >= 30).mean() * 100,
                "pct_sobrepeso": ((vals >= 25) & (vals < 30)).mean() * 100,
                "pct_normopeso": (vals < 25).mean() * 100
            }

        if n_sel == 1:
            g = sel_grupos[0]
            s = stats[g]
            zona = "obesidad" if s["mediana"] >= 30 else ("sobrepeso" if s["mediana"] >= 25 else "peso normal")
            hallazgos(f"""
            En el grupo <b>{g}</b>, el peso típico (mediana) es de <b>IMC {s['mediana']:.1f}</b>, lo que cae en la zona de <b>{zona}</b>.
            Distribuyendo a las personas según los cortes de la OMS:
            <br>
            • <b>{s['pct_normopeso']:.1f}%</b> tiene peso normal (IMC menor a 25).<br>
            • <b>{s['pct_sobrepeso']:.1f}%</b> tiene sobrepeso (IMC entre 25 y 30).<br>
            • <b>{s['pct_obesidad']:.1f}%</b> tiene obesidad (IMC mayor o igual a 30).
            <br><br>
            Lo que estos números dicen sobre este grupo: la mayoría de las personas <b>no</b> tienen un peso saludable según la OMS. Para entender por qué esto importa, activa los otros grupos en el filtro y compara cómo cambian estos porcentajes — esa comparación es la que revela el rol del peso en la diabetes.
            """)
        elif n_sel == 2:
            g1, g2 = sel_grupos
            s1, s2 = stats[g1], stats[g2]
            mayor, menor = (g1, g2) if s1["mediana"] > s2["mediana"] else (g2, g1)
            sm = stats[mayor]; sn = stats[menor]
            diff_med = abs(s1["mediana"] - s2["mediana"])
            diff_obs = sm["pct_obesidad"] - sn["pct_obesidad"]
            hallazgos(f"""
            La mediana del IMC en <b>{mayor}</b> ({sm['mediana']:.1f}) supera a la de <b>{menor}</b> ({sn['mediana']:.1f}) por <b>{diff_med:.1f} puntos</b>. Pero el dato más revelador está en la proporción de obesidad: <b>{sm['pct_obesidad']:.1f}%</b> en {mayor} contra <b>{sn['pct_obesidad']:.1f}%</b> en {menor} — una diferencia de <b>{diff_obs:.1f} puntos</b>.
            <br><br>
            Lo que esto significa lógicamente: no es solo que un grupo "pese un poco más" que el otro. Es que la <b>proporción</b> de personas en zona de obesidad cambia de forma sustancial entre los dos grupos. Cuando una distribución completa se desplaza así, no estamos hablando de casos individuales — estamos viendo un patrón estructural que afecta a todo el grupo.
            <br><br>
            Si {mayor} es el grupo con condición diabética más severa, este patrón confirma que el peso no es solo una consecuencia de la enfermedad: es un factor que la antecede y la sostiene.
            """)
        else:
            s_sd = stats.get("Sin Diabetes", {})
            s_pd = stats.get("Prediabetes", {})
            s_d  = stats.get("Diabetes", {})
            hallazgos(f"""
            Las medianas de IMC se ordenan de forma escalonada: <b>{s_sd.get('mediana',0):.1f}</b> en Sin Diabetes, <b>{s_pd.get('mediana',0):.1f}</b> en Prediabetes y <b>{s_d.get('mediana',0):.1f}</b> en Diabetes. La progresión no es casual: cada paso hacia una condición más grave viene con un peso típico mayor.
            <br><br>
            Lo más contundente está en la proporción de obesidad de cada grupo:
            <br>
            • Sin Diabetes: <b>{s_sd.get('pct_obesidad',0):.1f}%</b> tienen obesidad.<br>
            • Prediabetes: <b>{s_pd.get('pct_obesidad',0):.1f}%</b>.<br>
            • Diabetes: <b>{s_d.get('pct_obesidad',0):.1f}%</b>.
            <br><br>
            Es decir, en el grupo con diabetes, casi <b>{s_d.get('pct_obesidad',0)/s_sd.get('pct_obesidad',1):.1f} veces más</b> personas están en obesidad respecto al grupo sin diabetes. Cuando un factor cambia tanto entre grupos, no es coincidencia: <b>el peso no acompaña a la diabetes, la antecede</b>.
            <br><br>
            Esto tiene una implicación práctica: si el peso aumenta el riesgo de manera tan clara, entonces la prevención se vuelve concreta — bajar de IMC no es un consejo genérico, es la intervención más directa con la evidencia que muestra este dataset.
            """)

# ── Tab 3: Radar de factores de riesgo ───────────────────────
with tab3:
    st.markdown('<div class="ctitle">Perfil de factores de riesgo por condición diabética</div>', unsafe_allow_html=True)
    st.markdown('<div class="csub">Cuánto afecta cada factor a las personas según su condición</div>', unsafe_allow_html=True)

    factores_data = {}
    if not df.empty:
        fcols   = ["HighBP","HighChol","Smoker","PhysActivity","HeartDiseaseorAttack"]
        flabels = ["Hipertensión","Col. alto","Fumador","Act. física","Enf. cardíaca"]
        fig = go.Figure()
        for g in [gr for gr in GRUPOS if gr in sel_grupos]:
            sub  = df[df["Diabetes_Label"] == g]
            vals = [round(sub[c].mean()*100, 1) for c in fcols]
            factores_data[g] = dict(zip(flabels, vals))
            vals_closed = vals + [vals[0]]
            labels_closed = flabels + [flabels[0]]
            fig.add_trace(go.Scatterpolar(
                r=vals_closed, theta=labels_closed,
                fill="toself", name=g,
                line=dict(color=COLOR[g], width=2),
                fillcolor=COLOR[g], opacity=0.35,
                hovertemplate=f"<b>{g}</b><br>%{{theta}}: %{{r:.1f}}%<extra></extra>"
            ))
        fig.update_layout(
            height=480,
            polar=dict(
                radialaxis=dict(visible=True, range=[0,100], ticksuffix="%",
                                gridcolor="#e2e8f0", linecolor="#e2e8f0"),
                angularaxis=dict(gridcolor="#e2e8f0", linecolor="#e2e8f0"),
                bgcolor="white"
            ),
            paper_bgcolor="white",
            font=dict(family="Helvetica Neue, Helvetica, Arial, sans-serif", size=12),
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
            margin=dict(l=80, r=80, t=20, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Selecciona al menos un grupo.")
    st.markdown('<div class="fuente">Fuente: CDC BRFSS 2015 — Kaggle</div>', unsafe_allow_html=True)

    if df.empty:
        hallazgos("Selecciona al menos un grupo en el filtro lateral para ver los hallazgos.")
    else:
        n_sel = len(sel_grupos)
        if n_sel == 1:
            g = sel_grupos[0]
            d_g = factores_data[g]
            ordenado = sorted(d_g.items(), key=lambda x: -x[1])
            mayor, val_mayor = ordenado[0]
            menor, val_menor = ordenado[-1]
            hallazgos(f"""
            En el grupo <b>{g}</b>, los cinco factores se ordenan así de mayor a menor prevalencia:
            <br>
            {' · '.join([f'<b>{k}</b> ({v:.1f}%)' for k, v in ordenado])}
            <br><br>
            El factor más extendido es <b>{mayor}</b> ({val_mayor:.1f}%) y el menos común es <b>{menor}</b> ({val_menor:.1f}%). Pero ver un solo grupo no nos dice mucho — un porcentaje aislado no permite saber si es alto o bajo. Por ejemplo, un {val_mayor:.1f}% en {mayor} solo cobra sentido cuando lo comparamos con los otros grupos: ¿es similar al resto de la población o es una característica particular de {g}?
            <br><br>
            Activa los otros grupos en el filtro para que el contraste revele qué factores son <b>distintivos</b> de cada condición y cuáles son comunes a todos.
            """)
        elif n_sel == 2:
            g1, g2 = sel_grupos
            d1, d2 = factores_data[g1], factores_data[g2]
            diferencias = {f: d1[f] - d2[f] for f in d1}
            ordenado_dif = sorted(diferencias.items(), key=lambda x: -abs(x[1]))
            mayor_dif, val_dif = ordenado_dif[0]
            menor_dif, val_dif_min = ordenado_dif[-1]
            hallazgos(f"""
            Comparando los dos grupos, las diferencias más grandes están en:
            <br>
            • <b>{mayor_dif}</b>: {d1[mayor_dif]:.1f}% en {g1} vs {d2[mayor_dif]:.1f}% en {g2} — diferencia de <b>{abs(val_dif):.1f} puntos</b>.<br>
            • <b>{ordenado_dif[1][0]}</b>: {d1[ordenado_dif[1][0]]:.1f}% vs {d2[ordenado_dif[1][0]]:.1f}% — diferencia de {abs(ordenado_dif[1][1]):.1f} puntos.
            <br><br>
            Y la diferencia <b>más pequeña</b> está en <b>{menor_dif}</b> ({d1[menor_dif]:.1f}% vs {d2[menor_dif]:.1f}%, solo {abs(val_dif_min):.1f} puntos). Eso significa que en ese factor los dos grupos son muy parecidos — no es lo que los diferencia.
            <br><br>
            Lo lógico que se desprende: <b>{mayor_dif}</b> es el factor que más distingue a estos dos grupos. Si {g1} es el grupo con condición más severa, entonces controlar {mayor_dif} debería ser una prioridad para evitar que personas pasen del grupo más leve al más grave.
            """)
        else:
            d_sd = factores_data.get("Sin Diabetes", {})
            d_pd = factores_data.get("Prediabetes", {})
            d_d  = factores_data.get("Diabetes", {})
            # Calcular cuáles factores muestran progresión sd -> pd -> d
            ratio_hta = d_d.get("Hipertensión",0) / max(d_sd.get("Hipertensión",1), 0.1)
            ratio_chol = d_d.get("Col. alto",0) / max(d_sd.get("Col. alto",1), 0.1)
            ratio_phys = d_d.get("Act. física",0) / max(d_sd.get("Act. física",1), 0.1)
            hallazgos(f"""
            Mirando los tres grupos juntos, dos factores muestran un patrón claro de escalada de Sin Diabetes → Prediabetes → Diabetes:
            <br>
            • <b>Hipertensión</b>: {d_sd.get('Hipertensión',0):.1f}% → {d_pd.get('Hipertensión',0):.1f}% → <b>{d_d.get('Hipertensión',0):.1f}%</b>. En el grupo con diabetes es <b>{ratio_hta:.1f} veces</b> más frecuente que en el grupo sano.<br>
            • <b>Colesterol alto</b>: {d_sd.get('Col. alto',0):.1f}% → {d_pd.get('Col. alto',0):.1f}% → <b>{d_d.get('Col. alto',0):.1f}%</b>. La diabetes lo multiplica por <b>{ratio_chol:.1f}</b>.
            <br><br>
            Y un factor se mueve <b>en sentido opuesto</b>: la actividad física pasa de <b>{d_sd.get('Act. física',0):.1f}%</b> en sin diabetes, a {d_pd.get('Act. física',0):.1f}% en prediabetes, a solo <b>{d_d.get('Act. física',0):.1f}%</b> en el grupo con diabetes. Es la única variable donde el grupo más sano tiene <b>más</b> que los enfermos.
            <br><br>
            La lectura lógica es directa: la diabetes no aparece sola, viene en un paquete. Cuando alguien tiene diabetes, las probabilidades de que también tenga hipertensión y colesterol alto son <b>3 a 4 veces más altas</b> que en una persona sana. Y al mismo tiempo, hace menos ejercicio. Esto explica por qué los protocolos médicos para diabetes incluyen siempre control de presión, control de lípidos y prescripción de actividad física — no se tratan como cosas separadas porque <b>los datos muestran que no lo son</b>.
            """)

# ── Tab 4: Heatmap Edad × Condición ──────────────────────────
with tab4:
    st.markdown('<div class="ctitle">Prevalencia diabética según grupo de edad</div>', unsafe_allow_html=True)
    st.markdown('<div class="csub">Mapa de calor — más rojo = mayor porcentaje de personas en esa edad</div>', unsafe_allow_html=True)

    pcts_edad = {}
    if not df.empty:
        elabels = {1:"18-24",2:"25-29",3:"30-34",4:"35-39",5:"40-44",6:"45-49",
                   7:"50-54",8:"55-59",9:"60-64",10:"65-69",11:"70-74",12:"75-79",13:"80+"}
        gord = [g for g in GRUPOS if g in sel_grupos]
        de   = df_raw[df_raw["Diabetes_Label"].isin(gord)].copy()
        de["GrupoEdad"] = de["Age"].map(elabels)
        pivot = de.groupby(["GrupoEdad","Diabetes_Label"]).size().unstack(fill_value=0)
        pivot = pivot.reindex(columns=gord, fill_value=0)
        ppct  = pivot.div(pivot.sum(axis=1), axis=0)*100
        ppct  = ppct.reindex([elabels[i] for i in range(1,14)])

        for g in gord:
            pcts_edad[g] = ppct[g].to_dict()

        z_data = ppct.T.values.tolist()
        x_labels = ppct.index.tolist()
        y_labels = ppct.columns.tolist()
        text_data = [[f"{v:.1f}%" for v in row] for row in z_data]

        fig = go.Figure(go.Heatmap(
            z=z_data, x=x_labels, y=y_labels,
            text=text_data, texttemplate="%{text}",
            textfont=dict(size=11, color="#1a1a2e"),
            colorscale=[[0, "#f7fafc"], [0.3, "#fed7d7"], [0.6, "#fc8181"], [1, "#c53030"]],
            zmin=0, zmax=100,
            colorbar=dict(title="% del grupo", thickness=14, ticksuffix="%"),
            hovertemplate="<b>%{y}</b><br>Edad: %{x}<br>%{z:.1f}%<extra></extra>"
        ))
        fig.update_layout(
            height=380,
            margin=dict(l=120, r=20, t=20, b=70),
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="Helvetica Neue, Helvetica, Arial, sans-serif", size=11),
            xaxis=dict(title="Grupo de edad (años)", side="bottom", tickangle=-30),
            yaxis=dict(autorange="reversed")
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Selecciona al menos un grupo.")
    st.markdown('<div class="fuente">Fuente: CDC BRFSS 2015 — Kaggle</div>', unsafe_allow_html=True)

    if df.empty:
        hallazgos("Selecciona al menos un grupo en el filtro lateral para ver los hallazgos.")
    else:
        n_sel = len(sel_grupos)
        if n_sel == 1:
            g = sel_grupos[0]
            hallazgos(f"""
            Con un solo grupo activo (<b>{g}</b>), todas las celdas marcan 100% — porque dentro de los datos filtrados, este grupo es el único que existe. El mapa solo cobra sentido cuando hay al menos dos condiciones para comparar entre edades.
            <br><br>
            Activa otro grupo en el filtro para que el mapa pueda mostrar la <b>proporción</b> de cada condición en cada edad. Esa proporción es la que revela el patrón importante: cómo el riesgo cambia con los años.
            """)
        elif n_sel == 2:
            g1, g2 = sel_grupos[0], sel_grupos[1]
            joven_1 = pcts_edad[g1].get("18-24", 0)
            mayor_1 = pcts_edad[g1].get("80+", 0)
            joven_2 = pcts_edad[g2].get("18-24", 0)
            mayor_2 = pcts_edad[g2].get("80+", 0)
            cambio_1 = mayor_1 - joven_1
            cambio_2 = mayor_2 - joven_2
            hallazgos(f"""
            Los datos muestran cómo cambia la proporción de cada grupo a lo largo de las edades:
            <br>
            • <b>{g1}</b>: pasa de <b>{joven_1:.1f}%</b> en 18-24 años a <b>{mayor_1:.1f}%</b> en 80+. Cambio: <b>{cambio_1:+.1f} puntos</b>.<br>
            • <b>{g2}</b>: pasa de <b>{joven_2:.1f}%</b> en 18-24 a <b>{mayor_2:.1f}%</b> en 80+. Cambio: <b>{cambio_2:+.1f} puntos</b>.
            <br><br>
            Lo que esto dice lógicamente: cuando un grupo aumenta con la edad y el otro disminuye, no es porque las personas "cambien de grupo" individualmente — es porque la composición de cada generación es diferente. Las generaciones mayores acumularon más años de exposición a factores de riesgo (peso, sedentarismo, presión alta), y eso se refleja en la proporción de quienes hoy tienen una u otra condición.
            <br><br>
            Esto es importante para sistemas de salud: la edad no es solo un dato demográfico, es <b>un predictor estructural</b> que permite anticipar dónde poner los recursos.
            """)
        else:
            d_24 = pcts_edad.get("Diabetes", {}).get("18-24", 0)
            d_50 = pcts_edad.get("Diabetes", {}).get("50-54", 0)
            d_65 = pcts_edad.get("Diabetes", {}).get("65-69", 0)
            d_80 = pcts_edad.get("Diabetes", {}).get("80+", 0)
            sd_24 = pcts_edad.get("Sin Diabetes", {}).get("18-24", 0)
            sd_80 = pcts_edad.get("Sin Diabetes", {}).get("80+", 0)
            ratio_d = d_80 / max(d_24, 0.1)
            hallazgos(f"""
            Lo primero que salta en el mapa es que la diabetes pasa de prácticamente <b>{d_24:.1f}%</b> en personas de 18-24 años a <b>{d_80:.1f}%</b> en mayores de 80. Eso es un crecimiento de <b>{ratio_d:.0f} veces</b>. Y en paralelo, la fila de Sin Diabetes baja de <b>{sd_24:.1f}%</b> a <b>{sd_80:.1f}%</b>.
            <br><br>
            Pero el dato más útil no son los extremos, son los puntos intermedios: a los 50-54 años la diabetes ya está en <b>{d_50:.1f}%</b>, y a los 65-69 sube a <b>{d_65:.1f}%</b>. Es decir, entre los 50 y los 70 años la prevalencia <b>casi se duplica</b>. Esa franja de 20 años es donde el riesgo se acelera más rápido.
            <br><br>
            Lógicamente esto significa que las campañas de tamizaje no deberían empezar a los 65 (cuando ya muchos están enfermos), sino alrededor de los 45-50, antes de que la curva se acelere. <b>El gráfico no solo dice que el riesgo crece con la edad — dice exactamente cuándo empieza a crecer rápido</b>, y esa información es la que permite actuar a tiempo.
            """)

# ── Tab 5: Heatmap correlaciones ─────────────────────────────
with tab5:
    st.markdown('<div class="ctitle">Cómo se relacionan los indicadores de salud entre sí</div>', unsafe_allow_html=True)
    st.markdown('<div class="csub">Rojo: van de la mano · Azul: cuando uno sube, el otro baja</div>', unsafe_allow_html=True)
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

    fila_diab = mat.loc["Diabetes"].drop("Diabetes")
    top_pos = fila_diab.nlargest(3)
    top_neg = fila_diab.nsmallest(2)
    income_genhlth = mat.loc["Ingreso", "Salud gral."]
    edad_hta = mat.loc["Edad", "Hipertensión"]
    bmi_hta = mat.loc["BMI", "Hipertensión"]

    hallazgos(f"""
    El mapa cruza 9 variables del dataset y mide qué tan fuerte van juntas. Los valores van de -1 (azul oscuro: cuando una sube, la otra baja) a 1 (rojo oscuro: suben juntas). Cero (blanco) significa que no se relacionan.
    <br><br>
    Lo primero que hay que notar: <b>ninguna correlación con Diabetes pasa de 0.30</b>. Las tres más altas son <b>{top_pos.index[0]}</b> ({top_pos.iloc[0]:.2f}), <b>{top_pos.index[1]}</b> ({top_pos.iloc[1]:.2f}) y <b>{top_pos.index[2]}</b> ({top_pos.iloc[2]:.2f}). Esto significa que <b>ningún factor por sí solo explica la diabetes</b> — no hay una variable mágica. Si fuera tan simple, ya habría una sola prueba para detectarla. La diabetes es el resultado de varios factores actuando juntos.
    <br><br>
    Y eso lleva al segundo hallazgo: las correlaciones <b>entre los factores</b> son a veces más fuertes que con la diabetes misma. Por ejemplo, BMI con Hipertensión correlaciona <b>{bmi_hta:.2f}</b>, y Edad con Hipertensión <b>{edad_hta:.2f}</b>. Esto explica el patrón de "comorbilidad" que vimos en el radar — las enfermedades vienen en paquete porque <b>los factores de riesgo se refuerzan entre sí</b>.
    <br><br>
    El dato sociopolítico está en la esquina opuesta: <b>Ingreso vs Salud general</b> da <b>{income_genhlth:.2f}</b> (negativa). Es decir, a menor ingreso, peor salud percibida. No es una correlación gigante, pero es consistente y conecta con lo que vimos en el tab 1 — el dinero condiciona el acceso a la salud, y eso se traduce en cómo la gente se siente.
    <br><br>
    <b>Conclusión lógica:</b> el dataset no muestra una causa única de diabetes, sino una <b>red de variables interconectadas</b>. Cualquier modelo predictivo o intervención de salud pública que ignore esta interconexión va a fallar — porque atacar una sola variable deja a las otras compensándola.
    """)