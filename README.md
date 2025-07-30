
# Clasificador HealthFit

Una aplicación web moderna que utiliza agrupamiento KMeans para clasificar a los usuarios en distintos grupos de salud y acondicionamiento físico, basándose en su IMC y el número de pasos diarios.

## Funcionalidades

- **Interfaz moderna**: Diseño limpio y responsivo con TailwindCSS  
- **Clasificación de salud**: Ingresa tu IMC y pasos diarios para obtener una clasificación en grupos de salud  
- **Visualización interactiva**: Visualización del agrupamiento con Plotly  
- **Aprendizaje automático**: Agrupamiento KMeans con preprocesamiento de datos  
- **Lista para AWS**: Configurada para un despliegue sencillo en AWS EC2

## Grupos de Salud

1. **🚶‍♂️ Estilo de vida sedentario**: IMC elevado con bajos niveles de actividad  
2. **🏃‍♂️ Moderadamente activo**: IMC y niveles de actividad equilibrados  
3. **🏋️‍♂️ Altamente activo**: IMC óptimo con niveles altos de actividad  

## Instalación

1. **Clona o descarga el proyecto**
2. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Asegúrate de tener los archivos del modelo**:
   - Coloca los modelos entrenados en el directorio `model/`:
     - `model/kmeans_imc_pasos.pkl`
     - `model/scaler_imc_pasos.pkl`

4. **Ejecuta la aplicación**:
   ```bash
   python app.py
   ```

5. **Accede a la app**:
   - Abre tu navegador en `http://localhost:5000`

## Estructura del Proyecto

```
health_app/
├── app.py                          # Aplicación Flask
├── requirements.txt                # Dependencias de Python
├── README.md                       # Este archivo
├── templates/                      # Plantillas HTML
│   ├── base.html                   # Plantilla base con navegación
│   ├── index.html                  # Página principal
│   └── imc_pasos.html              # Página de clasificación
├── static/                         # Archivos estáticos
│   └── imc_pasos_clusters.html     # Visualización interactiva
├── model/                          # Archivos del modelo de ML
│   ├── kmeans_imc_pasos.pkl        # Modelo KMeans entrenado
│   └── scaler_imc_pasos.pkl        # Escalador de datos
└── Dataset_Salud_Wearables.csv     # Dataset usado para entrenamiento
```

## Uso

### Interfaz Web

1. **Inicio** (`/`): Vista general y navegación  
2. **Clasificación** (`/predict/imc_pasos`): Ingresa IMC y pasos para ser clasificado  
3. **Visualización** (`/visualization`): Gráfico interactivo de agrupamientos  

### Endpoints de la API

- `GET /`: Página de inicio  
- `GET /predict/imc_pasos`: Formulario de clasificación  
- `POST /predict/imc_pasos`: Enviar datos para clasificación  
- `GET /visualization`: Visualización interactiva con Plotly  

## Despliegue

### Despliegue en AWS EC2

1. **Lanza una instancia EC2** (Ubuntu/Amazon Linux)  
2. **Instala Python y pip**  
3. **Clona el repositorio**  
4. **Instala dependencias**: `pip install -r requirements.txt`  
5. **Instala y configura Gunicorn**:
   ```bash
   gunicorn --bind 0.0.0.0:5000 app:app
   ```
6. **Configura los grupos de seguridad** para permitir tráfico HTTP en el puerto 5000

### Consideraciones para Producción

- Usa un proxy inverso como nginx  
- Configura certificados SSL  
- Usa variables de entorno para datos sensibles  
- Usa un gestor de procesos como `systemd` o `supervisor`  
- Configura monitoreo y registros (logs)  

## Agregar Nuevos Modelos

La aplicación está diseñada para ser fácilmente expandible. Para agregar nuevos modelos de agrupamiento:

1. **Entrena tu modelo** y guárdalo como archivo `.pkl`  
2. **Crea nuevas rutas** en `app.py`  
3. **Agrega nuevas plantillas** para la interfaz del modelo  
4. **Actualiza la navegación** en `base.html`  
5. **Agrega descripciones del modelo** al diccionario de descripciones de clusters  

## Tecnologías Utilizadas

- **Backend**: Flask, scikit-learn, NumPy  
- **Frontend**: TailwindCSS, Font Awesome  
- **Visualización**: Plotly.js  
- **Despliegue**: Gunicorn (preparado para producción)

## Licencia

Este proyecto es de código abierto y está disponible bajo la Licencia MIT.
