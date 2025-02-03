# **Backend | IA - Segmentación de Video**

RestAPI desarrollada en Flask con integración de **Machine Learning** para segmentación de videos. Utiliza **Redes Neuronales Convolucionales (CNNs)** para eliminar fondos en tiempo real.  
**SMBD**: PostgreSQL.

## 📌 Resumen del Proyecto  

Este proyecto implementa un **sistema de segmentación de fondo en videos** basado en **aprendizaje profundo**, permitiendo remover fondos de manera precisa y eficiente. Utiliza un **modelo de segmentación U-Net** con una arquitectura basada en **ResNet50**, logrando una separación efectiva entre el sujeto y el fondo en cada frame de un video.  

A través de un **pipeline optimizado**, el sistema procesa cada frame del video, aplica un modelo preentrenado y genera una nueva versión del video con el fondo removido o reemplazado por un color específico.  
El backend está desarrollado en **Flask**, permitiendo la integración con bases de datos y almacenamiento de videos procesados.  

---

## 🧠 Tecnología y Modelado  

El modelo de segmentación está construido con **TensorFlow/Keras** y basado en **ResNet50**, utilizando las siguientes técnicas avanzadas:  

- 🔹 **Convoluciones Dilatadas**: Permiten capturar relaciones espaciales a diferentes escalas.  
- 🔹 **Bloques Residuales**: Mejoran la estabilidad del modelo y facilitan la propagación del gradiente.  
- 🔹 **U-Net con UpSampling**: Reconstruye la imagen segmentada con alta precisión.  

El sistema está optimizado para procesamiento en lotes y soporta paralelización con **ThreadPoolExecutor**, permitiendo una inferencia más rápida.  

---

## 🖥️ Infraestructura y Procesamiento  

El sistema sigue un flujo de trabajo bien estructurado:  

1️⃣ **Carga del Video** 📂  
   - El usuario sube un video a través del frontend o la API Flask.  

2️⃣ **Preprocesamiento** ⚙️  
   - El video se divide en frames individuales.  
   - Cada frame se redimensiona a **512x512** y se normaliza.  

3️⃣ **Segmentación de Fondo** 🧠  
   - Se aplica el modelo de segmentación a cada frame.  
   - Se genera una **máscara de segmentación** que diferencia el sujeto del fondo.  

4️⃣ **Postprocesamiento y Ensamblado** 🎬  
   - Se reconstruye el video con el fondo eliminado.  
   - Se genera una nueva versión del video en formatos **MP4 y WebM**.  

---

## 📚 ¿Por qué Redes Neuronales para la Segmentación?  

El uso de **redes neuronales convolucionales (CNNs)** permite obtener segmentaciones mucho más precisas que los enfoques tradicionales de eliminación de fondo. Algunas ventajas clave incluyen:  

✔️ **Mayor precisión**: Captura detalles en los bordes del sujeto.  
✔️ **Menos dependencia de condiciones de iluminación**: No requiere pantalla verde.  
✔️ **Escalabilidad**: Puede adaptarse a distintos tipos de videos y resoluciones.  

---

## 🔧 Tecnologías Utilizadas  

✅ **Backend:** Flask + SQLAlchemy  
✅ **Base de Datos:** PostgreSQL  
✅ **Machine Learning:** TensorFlow / Keras (ResNet50 + U-Net)  
✅ **Procesamiento de Video:** OpenCV  
✅ **Paralelización:** ThreadPoolExecutor  

---

## 🚀 Posibles Mejoras y Extensiones  

🔹 **Permitir reemplazo del fondo con otra imagen personalizada.**  
🔹 **Optimizar la inferencia con TensorRT para mayor velocidad.**  
🔹 **Agregar soporte para videos en 4K con segmentación más avanzada.**  

---

✍️ *Este proyecto representa un enfoque moderno y eficiente para la segmentación de videos con inteligencia artificial.*  
📢 *Contribuciones y mejoras son bienvenidas en el repositorio.* 🚀  
