# 📋 **Resumen Ejecutivo: Infraestructura y Despliegue**

## **🏗️ Infraestructura Utilizada**

### **Servicios AWS**
- **EC2**: Instancia virtual para alojar la aplicación
- **Ubuntu 24.04 LTS**: Sistema operativo del servidor
- **t2.micro**: Tipo de instancia (gratuita)

### **Componentes del Servidor**
- **Nginx**: Servidor web (proxy reverso)
- **Gunicorn**: Servidor WSGI para Python
- **Python 3.11**: Lenguaje de programación
- **Git**: Control de versiones

## **📝 Pasos Generales del Despliegue**

### **1. Preparación Local**
```bash
# Crear entorno virtual
python -m venv venv
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Probar aplicación localmente
python app.py
```

### **2. Configuración de AWS EC2**
- Crear instancia EC2 con Ubuntu
- Configurar grupo de seguridad (puertos 22, 80)
- Descargar archivo de clave (.pem)
- Conectar via SSH: `ssh -i clave.pem ubuntu@IP`

### **3. Instalación en el Servidor**
```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python y herramientas
sudo apt install -y python3 python3-venv nginx git

# Clonar repositorio
git clone https://github.com/mozunigaa/health-app.git
cd health-app
```

### **4. Configuración de la Aplicación**
```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Entrenar modelo
python retrain_model.py
```

### **5. Configuración de Servicios**
```bash
# Crear servicio systemd para Gunicorn
sudo nano /etc/systemd/system/health-app.service

# Configurar Nginx
sudo nano /etc/nginx/sites-available/health-app

# Activar servicios
sudo systemctl enable health-app
sudo systemctl start health-app
sudo systemctl restart nginx
```

### **6. Verificación**
```bash
# Verificar que todo funcione
sudo systemctl status health-app
sudo systemctl status nginx
curl http://localhost
```

## **🔄 Flujo de Actualizaciones**

### **Desarrollo Local**
1. Hacer cambios en el código
2. Probar localmente
3. Hacer commit y push a GitHub

### **Despliegue en Producción**
```bash
# Conectar al servidor
ssh -i clave.pem ubuntu@IP

# Actualizar código
cd health-app
git pull origin main

# Reiniciar aplicación
sudo systemctl restart health-app
```

## **📊 Resultado Final**

- **URL**: http://3.14.82.236
- **Aplicación**: Clasificador de salud con ML
- **Estado**: ✅ Funcionando en producción
- **Tecnologías**: Flask + scikit-learn + Nginx

## **🎯 Puntos Clave**

1. **Infraestructura simple**: Una instancia EC2
2. **Despliegue manual**: Git pull + restart
3. **Monitoreo básico**: systemctl status
4. **Escalabilidad**: Preparado para crecimiento futuro

---

**Tiempo total de implementación**: ~2 horas  
**Costo mensual**: $0 (Free Tier)  
**Complejidad**: Baja-Mediana

---

## **📋 Checklist de Despliegue**

### **Preparación**
- [ ] Repositorio en GitHub
- [ ] Archivo requirements.txt actualizado
- [ ] Aplicación funcionando localmente
- [ ] Clave SSH descargada

### **Configuración EC2**
- [ ] Instancia creada
- [ ] Grupo de seguridad configurado
- [ ] Conexión SSH exitosa
- [ ] Sistema actualizado

### **Instalación**
- [ ] Python instalado
- [ ] Nginx instalado
- [ ] Repositorio clonado
- [ ] Entorno virtual creado
- [ ] Dependencias instaladas

### **Configuración**
- [ ] Servicio systemd creado
- [ ] Nginx configurado
- [ ] Servicios iniciados
- [ ] Aplicación accesible

### **Verificación**
- [ ] Aplicación responde
- [ ] Modelo ML funciona
- [ ] Visualizaciones cargan
- [ ] Logs sin errores

---

## **🔧 Comandos Útiles**

### **Monitoreo**
```bash
# Ver estado de servicios
sudo systemctl status health-app
sudo systemctl status nginx

# Ver logs
sudo journalctl -u health-app -f
sudo tail -f /var/log/nginx/error.log
```

### **Mantenimiento**
```bash
# Reiniciar servicios
sudo systemctl restart health-app
sudo systemctl restart nginx

# Actualizar aplicación
cd health-app
git pull origin main
sudo systemctl restart health-app
```

### **Troubleshooting**
```bash
# Verificar puertos
sudo netstat -tlnp

# Verificar configuración Nginx
sudo nginx -t

# Verificar permisos
ls -la /home/ubuntu/health-app/
```

---

**Documento generado**: 30 de Julio, 2025  
**Proyecto**: Health PredictApp  
**Estudiante**: Monica  
**Universidad**: [Nombre de tu universidad] 