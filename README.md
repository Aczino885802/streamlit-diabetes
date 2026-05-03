# Diabetes Health Indicators — Streamlit App

## Descripción

Aplicación web interactiva desarrollada en Python con Streamlit y Plotly para explorar los indicadores de salud relacionados con la diabetes en la población adulta de Estados Unidos. Permite filtrar por condición diabética actualizando todas las visualizaciones en tiempo real, e incluye un bloque de **Hallazgos** debajo de cada gráfico que se recalcula dinámicamente según la selección del usuario.

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

1. **Acceso a salud condicionado por ingreso:** En el nivel de ingreso más bajo (<$10k), el 30.4% de las personas no fue al médico por costo, mientras que en el nivel más alto (>$75k) solo el 4% reporta esta barrera. Aunque la cobertura de seguro es alta en todos los niveles (76% a 96%), tener seguro no equivale a poder pagar la atención. Este patrón ayuda a explicar el subdiagnóstico de prediabetes en la población vulnerable.

2. **BMI como factor de riesgo central:** La mediana del IMC en personas con diabetes (~31, zona de obesidad según OMS) es significativamente mayor que en personas sin diabetes (~27, zona de sobrepeso). El histograma con cortes clínicos confirma que la distribución del peso se desplaza progresivamente hacia la derecha en los grupos con condición más severa.

3. **Hipertensión como comorbilidad dominante:** El 75.3% de las personas con diabetes también presenta hipertensión, frente al 37.1% en personas sin diabetes. La actividad física muestra el patrón inverso: 77.9% en sin diabetes vs 63.1% en diabetes. La diabetes no aparece aislada — viene acompañada de un paquete de comorbilidades cardiometabólicas.

4. **Prevalencia creciente con la edad:** La proporción de personas con diabetes aumenta sostenidamente con la edad. Entre los 50 y los 70 años la prevalencia casi se duplica, lo que define una franja crítica para programas de tamizaje preventivo.

5. **Correlaciones clave:** Diabetes correlaciona principalmente con salud general percibida (0.30), hipertensión (0.27) y BMI (0.22). La actividad física muestra correlación negativa consistente (−0.12). Ningún factor por sí solo explica la diabetes — es el resultado de múltiples variables interconectadas.

---

## Visualizaciones Implementadas

1. **Acceso a salud por ingreso (barras + línea)** — Cobertura de seguro de salud (`AnyHealthcare`) por nivel de ingreso cruzada con el porcentaje de personas que no fueron al médico por costo (`NoDocbcCost`). Revela la barrera económica al acceso médico real.

2. **Distribución del BMI con cortes OMS (histograma superpuesto)** — Distribución del IMC por condición diabética con líneas verticales que marcan los puntos de corte clínicos de la OMS: 25 (sobrepeso) y 30 (obesidad). Permite interpretar el peso en contexto clínico, no solo estadístico.

3. **Perfil de factores de riesgo (radar)** — Prevalencia de 5 factores de riesgo (hipertensión, colesterol, tabaquismo, actividad física, enfermedad cardíaca) representada como polígono cerrado por condición diabética. Muestra el "perfil completo" de cada grupo en una sola figura.

4. **Prevalencia por edad (mapa de calor)** — Porcentaje de cada condición diabética en 13 grupos etarios. La intensidad de color comunica el patrón de envejecimiento sin necesidad de leer todos los números.

5. **Mapa de correlaciones (heatmap)** — Matriz de correlación de Pearson entre 9 indicadores de salud con paleta divergente rojo–blanco–azul (escala −1 a 1).

Cada visualización incluye un bloque de **Hallazgos** dinámico que se actualiza según los filtros seleccionados, calculando porcentajes, medianas y ratios directamente desde el CSV.

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

- Carlos Andrés Muñoz Arias
- Juan Camilo Girata Arango

**Curso:** Herramientas y Visualización de Datos
**Institución:** Fundación Universitaria Los Libertadores
**Año:** 2026