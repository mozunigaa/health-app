import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import os

# Cargar el dataset
print("Cargando dataset...")
df = pd.read_csv('Dataset_Salud_Wearables.csv')

# Selección de características
X = df[['imc', 'pasos_diarios']].values

# Estandarización
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Entrenar modelo KMeans con los parámetros exactos de Colab
print("Entrenando modelo KMeans...")
k_opt = 3
kmeans = KMeans(n_clusters=k_opt, init='k-means++', n_init=10, random_state=0)
cluster_labels = kmeans.fit_predict(X_scaled)

# Calcular la puntuación silhouette
silhouette_avg = silhouette_score(X_scaled, cluster_labels)
print(f'Puntuación promedio silhouette para k={k_opt}: {silhouette_avg:.4f}')

# Guardar el modelo y scaler
print("Guardando modelo...")
if not os.path.exists('model'):
    os.makedirs('model')

with open('model/kmeans_imc_pasos.pkl', 'wb') as f:
    pickle.dump(kmeans, f)

with open('model/scaler_imc_pasos.pkl', 'wb') as f:
    pickle.dump(scaler, f)

print("Modelo guardado exitosamente!")

# Crear visualización interactiva completa en español
print("Creando visualización completa...")

# Crear DataFrame para la visualización
df_viz = pd.DataFrame({
    'IMC': X[:, 0],
    'Pasos_Diarios': X[:, 1],
    'Cluster': cluster_labels
})

# Mapear clusters a nombres en español
cluster_names = {
    0: 'Estilo de Vida Sedentario',
    1: 'Moderadamente Activo', 
    2: 'Altamente Activo'
}

df_viz['Grupo_Salud'] = df_viz['Cluster'].map(cluster_names)

# Colores para los clusters
colors = ['#ef4444', '#f59e0b', '#10b981']  # Rojo, Amarillo, Verde

# Crear figura con subplots
fig = make_subplots(
    rows=2, cols=1,
    subplot_titles=('Clasificación de Salud: IMC vs Pasos Diarios', 'Descripción de los Grupos de Salud'),
    specs=[[{"type": "scatter"}],
           [{"type": "table"}]],
    vertical_spacing=0.1,
    row_heights=[0.7, 0.3]
)

# Agregar gráfico de dispersión
for i, cluster_name in enumerate(cluster_names.values()):
    cluster_data = df_viz[df_viz['Grupo_Salud'] == cluster_name]
    fig.add_trace(
        go.Scatter(
            x=cluster_data['IMC'],
            y=cluster_data['Pasos_Diarios'],
            mode='markers',
            name=cluster_name,
            marker=dict(color=colors[i], size=8),
            hovertemplate='<b>%{fullData.name}</b><br>' +
                         'IMC: %{x:.1f}<br>' +
                         'Pasos: %{y:,.0f}<br>' +
                         '<extra></extra>'
        ),
        row=1, col=1
    )

# Agregar centroides
centroids = kmeans.cluster_centers_
centroids_unscaled = scaler.inverse_transform(centroids)

for i, (centroid, name) in enumerate(zip(centroids_unscaled, cluster_names.values())):
    fig.add_trace(
        go.Scatter(
            x=[centroid[0]],
            y=[centroid[1]],
            mode='markers',
            marker=dict(
                symbol='x',
                size=15,
                color=colors[i],
                line=dict(width=3, color='black')
            ),
            name=f'Centroide: {name}',
            showlegend=True,
            hovertemplate=f'<b>Centroide: {name}</b><br>' +
                         f'IMC: {centroid[0]:.1f}<br>' +
                         f'Pasos: {centroid[1]:,.0f}<br>' +
                         '<extra></extra>'
        ),
        row=1, col=1
    )

# Crear tabla con descripciones de clusters
cluster_stats = []
for cluster_id in range(k_opt):
    cluster_data = df_viz[df_viz['Cluster'] == cluster_id]
    cluster_name = cluster_names[cluster_id]
    
    # Descripciones personalizadas basadas en los datos
    if cluster_id == 0:  # Sedentario
        description = "Baja actividad física con IMC más alto. Considera aumentar los pasos diarios y mantener una dieta equilibrada."
        icon = "🚶‍♂️"
    elif cluster_id == 1:  # Moderadamente Activo
        description = "Buen equilibrio entre IMC y actividad diaria. ¡Sigue así!"
        icon = "🏃‍♂️"
    else:  # Altamente Activo
        description = "Excelente perfil de fitness con IMC óptimo y altos niveles de actividad."
        icon = "🏋️‍♂️"
    
    cluster_stats.append([
        f"{icon} {cluster_name}",
        f"{len(cluster_data)} personas",
        f"IMC: {cluster_data['IMC'].mean():.1f}",
        f"Pasos: {cluster_data['Pasos_Diarios'].mean():,.0f}",
        description
    ])

# Agregar tabla
fig.add_trace(
    go.Table(
        header=dict(
            values=['Grupo de Salud', 'Cantidad', 'IMC Promedio', 'Pasos Promedio', 'Descripción'],
            fill_color='#10b981',
            font=dict(color='white', size=12),
            align='left'
        ),
        cells=dict(
            values=list(zip(*cluster_stats)),
            fill_color='white',
            font=dict(size=11),
            align='left',
            height=30
        ),
        columnwidth=[0.2, 0.1, 0.1, 0.1, 0.5]
    ),
    row=2, col=1
)

# Actualizar layout
fig.update_layout(
    title={
        'text': 'HealthFit Classifier - Análisis de Clusters de Salud',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 24, 'color': '#064e3b'}
    },
    plot_bgcolor='white',
    width=1000,
    height=800,
    showlegend=True,
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    )
)

# Actualizar ejes del gráfico
fig.update_xaxes(
    title_text='Índice de Masa Corporal (IMC)',
    showgrid=True,
    gridwidth=1,
    gridcolor='lightgray',
    row=1, col=1
)
fig.update_yaxes(
    title_text='Pasos Diarios',
    showgrid=True,
    gridwidth=1,
    gridcolor='lightgray',
    row=1, col=1
)

# Actualizar tabla
fig.update_xaxes(visible=False, row=2, col=1)
fig.update_yaxes(visible=False, row=2, col=1)

# Guardar la visualización
if not os.path.exists('static'):
    os.makedirs('static')

fig.write_html('static/imc_pasos_clusters.html')
print("Visualización completa guardada en static/imc_pasos_clusters.html")

# Mostrar estadísticas de los clusters
print("\nEstadísticas de los clusters:")
for cluster_id in range(k_opt):
    cluster_data = df_viz[df_viz['Cluster'] == cluster_id]
    print(f"\n{cluster_names[cluster_id]}:")
    print(f"  - Cantidad de personas: {len(cluster_data)}")
    print(f"  - IMC promedio: {cluster_data['IMC'].mean():.2f}")
    print(f"  - Pasos promedio: {cluster_data['Pasos_Diarios'].mean():.0f}")

print("\n¡Proceso completado exitosamente!") 