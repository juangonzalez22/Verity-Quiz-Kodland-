# Verity Quiz

**Verity Quiz** es un bot interactivo de trivia para Discord desarrollado en Python utilizando la biblioteca `discord.py`. El bot permite a los usuarios participar en juegos de preguntas y respuestas en tiempo real mediante botones interactivos, competir en un ranking de puntuaciones y visualizar sus estadísticas de precisión. Además, integra la API de GIPHY para animar las respuestas y *The Trivia API* para generar preguntas ilimitadas de forma dinámica.

---

## Características Principales

- **Preguntas en Tiempo Real:** Obtiene preguntas de opción múltiple de *The Trivia API* de forma automática.
- **Modo Respaldo (Fallback):** Si la API externa falla o no responde, el bot carga automáticamente preguntas desde un archivo local.
- **Botones Interactivos:** Utiliza componentes de interfaz de Discord para seleccionar las respuestas.
- **Control de Acceso y Tiempo:** Cada pregunta está asignada únicamente al usuario que ejecutó el comando y expira automáticamente tras un tiempo límite.
- **Integración con GIPHY:** Muestra GIFs animados según el estado del juego.
- **Sistema de Puntuación y Ranking:** Registra los puntos, aciertos totales y precisión de cada usuario de forma persistente en `scores.json`.
- **Estructura Modular:** Organizado mediante *Cogs* y servicios independientes para facilitar el mantenimiento y la escalabilidad del código.

---

## Requisitos Previos

- Python 3.10 o superior.
- Token de Bot de Discord.
- Clave de API de GIPHY (opcional, para habilitar los GIFs animados).

---