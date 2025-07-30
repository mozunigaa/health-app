# HealthFit Classifier

A modern web application that uses KMeans clustering to classify users into different health and fitness groups based on their BMI and daily step count.

## Features

- **Modern UI**: Clean, responsive design with TailwindCSS
- **Health Classification**: Input BMI and daily steps to get classified into health groups
- **Interactive Visualization**: Plotly-powered clustering visualization
- **Machine Learning**: KMeans clustering with data preprocessing
- **AWS Ready**: Configured for easy deployment on AWS EC2

## Health Groups

1. **🚶‍♂️ Sedentary Lifestyle**: Higher BMI with lower activity levels
2. **🏃‍♂️ Moderately Active**: Balanced BMI and activity levels  
3. **🏋️‍♂️ Highly Active**: Optimal BMI with high activity levels

## Installation

1. **Clone or download the project**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure model files exist**:
   - Place your trained models in the `model/` directory:
     - `model/kmeans_imc_pasos.pkl`
     - `model/scaler_imc_pasos.pkl`

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the app**:
   - Open your browser to `http://localhost:5000`

## Project Structure

```
health_app/
├── app.py                          # Flask application
├── requirements.txt                # Python dependencies
├── README.md                      # This file
├── templates/                     # HTML templates
│   ├── base.html                 # Base template with navigation
│   ├── index.html                # Homepage
│   └── imc_pasos.html           # Classification page
├── static/                       # Static files
│   └── imc_pasos_clusters.html  # Interactive visualization
├── model/                        # ML model files
│   ├── kmeans_imc_pasos.pkl     # Trained KMeans model
│   └── scaler_imc_pasos.pkl     # Data scaler
└── Dataset_Salud_Wearables.csv  # Training dataset
```

## Usage

### Web Interface

1. **Homepage** (`/`): Overview and navigation
2. **Classification** (`/predict/imc_pasos`): Input BMI and steps for classification
3. **Visualization** (`/visualization`): Interactive clustering chart

### API Endpoints

- `GET /`: Homepage
- `GET /predict/imc_pasos`: Classification form
- `POST /predict/imc_pasos`: Submit data for classification
- `GET /visualization`: Interactive Plotly visualization

## Deployment

### AWS EC2 Deployment

1. **Launch EC2 instance** (Ubuntu/Amazon Linux)
2. **Install Python and pip**
3. **Clone the repository**
4. **Install dependencies**: `pip install -r requirements.txt`
5. **Install and configure Gunicorn**:
   ```bash
   gunicorn --bind 0.0.0.0:5000 app:app
   ```
6. **Configure security groups** to allow HTTP traffic on port 5000

### Production Considerations

- Use a reverse proxy (nginx) for production
- Set up SSL certificates
- Configure environment variables for sensitive data
- Use a process manager like systemd or supervisor
- Set up monitoring and logging

## Adding New Models

The application is designed to be easily expandable. To add new clustering models:

1. **Train your model** and save as `.pkl` files
2. **Create new routes** in `app.py`
3. **Add new templates** for the model interface
4. **Update navigation** in `base.html`
5. **Add model descriptions** to the cluster descriptions dictionary

## Technologies Used

- **Backend**: Flask, scikit-learn, NumPy
- **Frontend**: TailwindCSS, Font Awesome
- **Visualization**: Plotly.js
- **Deployment**: Gunicorn (production ready)

## License

This project is open source and available under the MIT License.
