# Diabetes Health Indicators — Streamlit App

## Descripción

Aplicación web interactiva desarrollada en Python con Streamlit y Plotly para explorar los indicadores de salud relacionados con la diabetes en la población adulta de Estados Unidos. Permite filtrar por condición diabética actualizando todas las visualizaciones en tiempo real.

**Proyecto 2 — Herramientas y Visualización de Datos**
Fundación Universitaria Los Libertadores

---

## Dataset

- **Fuente:** Kaggle / CDC (Centers for Disease Control and Prevention)
- **URL:** https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset
- **Nombre:** Diabetes Health Indicators Dataset — BRFSS 2015
- **Descripción:** Encuesta telefónica aplicada por el CDC a adultos en EE.UU. durante 2015. Contiene 253,680 registros y 22 variables relacionadas con condiciones de salud, hábitos de vida e indicadores clínicos. La variable objetivo (`Diabetes_012`) clasifica a cada persona en: sin diabetes (0), prediabetes (1) o diabetes (2).

---

## Hallazgos Principales

1. **Subdiagnóstico de prediabetes:** Solo el 1.8% de los encuestados reporta prediabetes, lo que sugiere un alto nivel de subdiagnóstico en la población general estadounidense.

2. **BMI como factor de riesgo central:** La mediana del IMC en personas con diabetes (~31) es significativamente mayor que en personas sin diabetes (~27), confirmando la obesidad como factor de riesgo principal.

3. **Hipertensión como comorbilidad dominante:** El 75.3% de las personas con diabetes también presenta hipertensión, frente al 37.1% en personas sin diabetes.

4. **Prevalencia creciente con la edad:** La proporción de personas con diabetes aumenta sostenidamente con la edad. A partir del grupo 60–64 años, los casos superan el 25% de los encuestados en ese rango.

5. **Correlaciones clave:** Diabetes correlaciona principalmente con salud general percibida (0.30), hipertensión (0.27) y BMI (0.22). La actividad física muestra correlación negativa consistente (−0.12).

---

## Visualizaciones Implementadas

1. **Gráfico de barras comparativo** — Distribución de encuestados por condición diabética con conteos absolutos y porcentajes, recalculados en tiempo real al aplicar filtros.

2. **Diagrama de caja (boxplot)** — Distribución del IMC por grupo con mediana, rango intercuartílico, bigotes (1.5×IQR) y media calculados desde el CSV.

3. **Barras agrupadas** — Prevalencia de 5 factores de riesgo (hipertensión, colesterol, tabaquismo, actividad física, enfermedad cardíaca) por condición diabética.

4. **Barras apiladas al 100%** — Composición de la condición diabética según 13 grupos de edad, mostrando la evolución de la prevalencia a lo largo del ciclo de vida.

5. **Mapa de calor (heatmap)** — Matriz de correlación de Pearson entre 9 indicadores de salud con paleta divergente rojo–blanco–azul.

---

## Tecnologías Utilizadas

- **Framework:** Streamlit 1.56.0
- **Lenguaje:** Python 3.11
- **Bibliotecas:**
  - `streamlit` — framework de aplicaciones web
  - `pandas` — manipulación y análisis de datos
  - `numpy` — cálculos numéricos
  - `plotly` — visualizaciones interactivas

---

## Instalación y Ejecución Local

### Requisitos Previos

- Python >= 3.9
- pip

### Instrucciones

```bash
# Clonar repositorio
git clone https://github.com/Aczino885802/streamlit-diabetes.git
cd streamlit-diabetes

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python -m streamlit run app.py
```

El dataset debe estar ubicado en `data/diabetes_012_health_indicators_BRFSS2015.csv`.

---

## Despliegue

**URL en producción:** https://diabetes-brfss-2015.streamlit.app

Desplegado en **Streamlit Community Cloud** desde la rama `main`.

---

## Autores

- Carlos Muñoz
- [Juan Camilo]

**Curso:** Herramientas y Visualización de Datos
**Institución:** Fundación Universitaria Los Libertadores
**Año:** 2026
