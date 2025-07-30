from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import os

app = Flask(__name__)

# Load the trained models
def load_models():
    """Load the KMeans model and scaler"""
    try:
        with open('model/kmeans_imc_pasos.pkl', 'rb') as f:
            kmeans_model = pickle.load(f)
        with open('model/scaler_imc_pasos.pkl', 'rb') as f:
            scaler = pickle.load(f)
        return kmeans_model, scaler
    except FileNotFoundError as e:
        print(f"Model files not found: {e}")
        return None, None

# Load models at startup
kmeans_model, scaler = load_models()

# Cluster descriptions for better user understanding
CLUSTER_DESCRIPTIONS = {
    0: {
        "name": "Estilo de Vida Sedentario",
        "description": "Baja actividad física con IMC más alto. Considera aumentar los pasos diarios y mantener una dieta equilibrada.",
        "color": "bg-red-100 text-red-800 border-red-200",
        "icon": "🚶‍♂️"
    },
    1: {
        "name": "Moderadamente Activo",
        "description": "Buen equilibrio entre IMC y actividad diaria. ¡Sigue así!",
        "color": "bg-yellow-100 text-yellow-800 border-yellow-200",
        "icon": "🏃‍♂️"
    },
    2: {
        "name": "Altamente Activo",
        "description": "Excelente perfil de fitness con IMC óptimo y altos niveles de actividad.",
        "color": "bg-green-100 text-green-800 border-green-200",
        "icon": "🏋️‍♂️"
    }
}

@app.route('/')
def index():
    """Homepage with project description and navigation"""
    return render_template('index.html')

@app.route('/predict/imc_pasos', methods=['GET', 'POST'])
def predict_imc_pasos():
    """Classification page for IMC and daily steps"""
    if request.method == 'GET':
        return render_template('imc_pasos.html')
    
    if request.method == 'POST':
        try:
            # Get form data
            imc = float(request.form.get('imc'))
            pasos = float(request.form.get('pasos'))
            
            if kmeans_model is None or scaler is None:
                return render_template('imc_pasos.html', 
                                     error="Archivos del modelo no encontrados. Por favor, asegúrate de que los archivos del modelo estén en la ubicación correcta.")
            
            # Prepare data for prediction
            user_data = np.array([[imc, pasos]])
            
            # Scale the data
            user_data_scaled = scaler.transform(user_data)
            
            # Make prediction
            cluster = kmeans_model.predict(user_data_scaled)[0]
            
            # Get cluster information
            cluster_info = CLUSTER_DESCRIPTIONS.get(cluster, {
                "name": f"Grupo {cluster}",
                "description": "Clasificación completada.",
                "color": "bg-blue-100 text-blue-800 border-blue-200",
                "icon": "📊"
            })
            
            return render_template('imc_pasos.html', 
                                 prediction=True,
                                 cluster=cluster,
                                 cluster_info=cluster_info,
                                 imc=imc,
                                 pasos=pasos)
            
        except ValueError:
            return render_template('imc_pasos.html', 
                                 error="Por favor, ingresa valores numéricos válidos para IMC y pasos diarios.")
        except Exception as e:
            return render_template('imc_pasos.html', 
                                 error=f"Ocurrió un error: {str(e)}")

@app.route('/visualization')
def visualization():
    """Serve the interactive Plotly visualization"""
    return app.send_static_file('imc_pasos_clusters.html')

if __name__ == '__main__':
    # Ensure model directory exists
    if not os.path.exists('model'):
        print("Warning: Model directory not found. Please ensure model files are available.")
    
    # Ensure static directory exists
    if not os.path.exists('static'):
        os.makedirs('static')
    
    # Ensure templates directory exists
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    app.run(debug=True, host='0.0.0.0', port=5000)
