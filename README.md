# Análisis de Portafolios de Acciones

Este proyecto es un microservicio para analizar y optimizar portafolios de acciones, desarrollado en Python y desplegado en AWS EC2. Calcula métricas financieras clave como el retorno anualizado, volatilidad y ratio Sharpe, y ofrece una interfaz web interactiva con Streamlit para visualizar datos y resultados.

🌐 **Demo en vivo**: [http://13.59.225.151:8501](http://13.59.225.151:8501)  
📂 **Código fuente**: [GitHub](https://github.com/luissar32/portfolio_analysis)

## Características
- Carga datos de acciones en tiempo real usando `yfinance` o subiendo un archivo CSV.
- Calcula métricas financieras: retorno anualizado, volatilidad, ratio Sharpe.
- Visualiza retornos acumulados, frontera eficiente y pesos óptimos del portafolio.
- Interfaz web con tema oscuro personalizado para una experiencia visual elegante.
- Desplegado en AWS EC2 para acceso público.

## Instalación (Entorno Local)
1. Clona el repositorio: https://github.com/luissar32/portfolio_analysis.git
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