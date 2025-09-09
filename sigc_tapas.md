# 📘 Manual del Sistema Integrado de Gestión de la Calidad (SIGC)  
**Proyecto: Clasificación de Tapas mediante Visión Artificial**

---

## 1. Introducción
Este manual documenta el **Sistema Integrado de Gestión de la Calidad (SIGC)** aplicado al proyecto de clasificación automática de tapas de envases utilizando inteligencia artificial (IA) y redes neuronales convolucionales (YOLOv8).  
El propósito es garantizar la **calidad, trazabilidad, confiabilidad y mejora continua** del sistema.

---

## 2. Alcance
El SIGC abarca:
- Procesamiento de imágenes de tapas.
- Clasificación en dos categorías: **Intacta** y **Dañada**.
- Gestión del dataset y anotaciones.
- Entrenamiento, validación y despliegue del modelo.
- Uso de la aplicación web en **Streamlit** para la clasificación.
- Gestión documental de resultados y reportes.

No incluye actividades de producción física ni embalaje de productos, solo el control digital de calidad de tapas.

---

## 3. Objetivos del SIGC
1. Garantizar que el modelo de clasificación cumpla estándares de calidad (≥90% de precisión en validación).  
2. Asegurar la integridad del dataset (CSV, imágenes, etiquetas YOLO).  
3. Establecer trazabilidad de versiones de modelo (`best.pt`, `ultimo_resultado.json`).  
4. Implementar procesos de mejora continua basados en métricas de desempeño.  
5. Cumplir con requisitos legales y normativos en gestión de datos.  

---

## 4. Política de Calidad
La organización se compromete a:
- Implementar controles de calidad en todo el ciclo de vida del sistema.  
- Mantener la confidencialidad e integridad de los datos.  
- Usar metodologías reproducibles y documentadas.  
- Fomentar la innovación tecnológica en la detección de defectos.  

---

## 5. Procesos del SIGC

### 5.1. Entrada de datos
- Anotaciones en formato **CSV (VIA/VGG)**.  
- Imágenes en carpeta `IMAGENES/`.  
- Validación automática de columnas (`filename`, `class`, `bbox`).  

### 5.2. Procesamiento
- Conversión de anotaciones a formato YOLO.  
- Generación de dataset estructurado (`train/`, `val/`).  
- Creación de `data.yaml` para entrenamiento.  

### 5.3. Entrenamiento
- Ejecución de `train.py` con parámetros controlados (`epochs`, `batch`, `imgsz`).  
- Registro de resultados en `runs/detect/train/`.  

### 5.4. Clasificación
- Uso de `app.py` en Streamlit para detección en imágenes nuevas.  
- Visualización de resultados y exportación a `ultimo_resultado.json`.  

### 5.5. Salidas
- Reporte gráfico de métricas (precisión, recall, pérdida).  
- Predicciones etiquetadas en imágenes.  
- Pesos del modelo (`best.pt`, `last.pt`).  

---

## 6. Roles y Responsabilidades
- **Administrador del Sistema:** Responsable de configurar el entorno y versionado del modelo.  
- **Equipo de QA:** Verifica calidad de dataset, etiquetas y resultados.  
- **Usuarios finales:** Suben imágenes a la app Streamlit y consultan resultados.  
- **Responsable SIGC:** Documenta procesos, gestiona auditorías y asegura la mejora continua.  

---

## 7. Control Documental
- Los archivos principales se encuentran en:  
  - `sigc_tapas.md` → Manual de calidad.  
  - `train.py` → Script de entrenamiento.  
  - `app.py` → Aplicación de clasificación.  
  - `jarlids_annots.csv` → Anotaciones iniciales.  
  - `ultimo_resultado.json` → Último resultado de predicción.  

- Todo el repositorio se versiona en **GitHub**.  
- Los datasets se gestionan bajo control de cambios.  

---

## 8. Mejora Continua
- Revisar métricas de entrenamiento cada ciclo.  
- Ajustar parámetros de YOLO según desviaciones.  
- Auditorías trimestrales sobre dataset y resultados.  
- Feedback de usuarios integrado al pipeline de mejoras.  

---

## 9. Gestión de Riesgos
- **Riesgo:** Dataset corrupto o incompleto → **Mitigación:** validación automática en `train.py`.  
- **Riesgo:** Baja precisión del modelo → **Mitigación:** aumento de dataset y reentrenamiento.  
- **Riesgo:** Pérdida de trazabilidad → **Mitigación:** versionado Git y control de commits.  
- **Riesgo:** Fallo en despliegue → **Mitigación:** redundancia en entornos (local + nube).  

---

## 10. Indicadores de Desempeño
- Precisión del modelo en validación (`mAP@0.5`).  
- Porcentaje de imágenes mal clasificadas.  
- Tiempo promedio de inferencia.  
- Frecuencia de actualizaciones de dataset.  

---

## 11. Auditorías
- Internas: cada 3 meses sobre calidad de dataset y código.  
- Externas: anuales, verificando cumplimiento con estándares ISO 9001 aplicados a software.  

---

## 12. Conclusiones
El **SIGC Tapas** garantiza que el sistema de clasificación basado en visión artificial cumpla criterios de calidad, trazabilidad y mejora continua, aportando confiabilidad al control de tapas en la línea de producción.
