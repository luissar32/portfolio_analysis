# Análisis de Cartera de Acciones

Este proyecto analiza el rendimiento de una cartera de acciones usando Python. Calcula métricas financieras como el rendimiento anualizado, volatilidad y ratio Sharpe, y genera una página HTML con gráficos interactivos.

## Instalación
1. Clona el repositorio: `git clone https://github.com/<tu-usuario>/<nombre-repositorio>.git`
2. Instala las dependencias: `pip install -r requirements.txt`
3. Ejecuta el script: `python app.py`

## Resultados
- Genera un archivo `index.html` con métricas y gráficos.
- Aloja la página en GitHub Pages.

## Tecnologías
- Python
- yfinance
- pandas
- numpy
- plotly

## Aplicación Streamlit

Una interfaz web para el análisis de portafolios está disponible en el directorio `frontend/`.

### Ejecutar en Streamlit Cloud
1. Conecta este repositorio y selecciona la rama `feature/porfolioAnalysis_v0.1_20250510`.
3. Configura `frontend/main.py` como punto de entrada.
4. Accede a la URL generada para probar la aplicación.

### Funcionalidades
- Carga datos de acciones vía `yfinance` o CSV.
- Calcula métricas como retorno anualizado y Sharpe ratio.
- Visualiza retornos acumulados y la frontera eficiente.
- Muestra pesos óptimos del portafolio.