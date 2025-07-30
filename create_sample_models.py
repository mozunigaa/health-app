#!/usr/bin/env python3
"""
Script to create sample KMeans model and scaler for testing the health classification app.
This creates realistic models based on typical BMI and daily steps data.
"""

import pickle
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os

def create_sample_models():
    """Create sample KMeans model and scaler for testing"""
    
    # Create sample data that represents realistic BMI and daily steps
    np.random.seed(42)  # For reproducible results
    
    # Generate sample data for 3 clusters
    # Cluster 0: Sedentary (higher BMI, lower steps)
    cluster0_bmi = np.random.normal(30, 3, 100)  # BMI around 30
    cluster0_steps = np.random.normal(3500, 1000, 100)  # Steps around 3500
    
    # Cluster 1: Moderately Active (moderate BMI, moderate steps)
    cluster1_bmi = np.random.normal(25, 2, 100)  # BMI around 25
    cluster1_steps = np.random.normal(7000, 1500, 100)  # Steps around 7000
    
    # Cluster 2: Highly Active (lower BMI, higher steps)
    cluster2_bmi = np.random.normal(21, 2, 100)  # BMI around 21
    cluster2_steps = np.random.normal(13000, 2000, 100)  # Steps around 13000
    
    # Combine all data
    X = np.column_stack([
        np.concatenate([cluster0_bmi, cluster1_bmi, cluster2_bmi]),
        np.concatenate([cluster0_steps, cluster1_steps, cluster2_steps])
    ])
    
    # Ensure reasonable bounds
    X[:, 0] = np.clip(X[:, 0], 15, 45)  # BMI between 15-45
    X[:, 1] = np.clip(X[:, 1], 1000, 25000)  # Steps between 1000-25000
    
    # Create and fit the scaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Create and fit KMeans model
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    
    # Create model directory if it doesn't exist
    os.makedirs('model', exist_ok=True)
    
    # Save the models
    with open('model/kmeans_imc_pasos.pkl', 'wb') as f:
        pickle.dump(kmeans, f)
    
    with open('model/scaler_imc_pasos.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    print("✅ Sample models created successfully!")
    print(f"📊 KMeans model: 3 clusters")
    print(f"📏 Scaler: StandardScaler fitted on {len(X)} samples")
    print(f"💾 Files saved:")
    print(f"   - model/kmeans_imc_pasos.pkl")
    print(f"   - model/scaler_imc_pasos.pkl")
    
    # Test the models
    print("\n🧪 Testing models with sample data:")
    test_data = np.array([[25.0, 8000], [30.0, 3000], [20.0, 15000]])
    test_scaled = scaler.transform(test_data)
    predictions = kmeans.predict(test_scaled)
    
    for i, (bmi, steps) in enumerate(test_data):
        print(f"   BMI: {bmi}, Steps: {steps:,} → Cluster: {predictions[i]}")

if __name__ == "__main__":
    create_sample_models()
