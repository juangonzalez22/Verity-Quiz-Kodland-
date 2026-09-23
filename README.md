# Verity Quiz

**Verity Quiz** es un bot interactivo de trivia para Discord desarrollado en Python con `discord.py` y una interfaz web ligera construida con **Flask**. El bot permite a los usuarios participar en juegos de preguntas y respuestas en tiempo real mediante botones interactivos, competir en un ranking de puntuaciones y visualizar sus estadísticas. Además, integra la API de GIPHY para animar las respuestas, *The Trivia API* para generar preguntas dinámicas, y un servidor web integrado para mantener el servicio activo 24/7 en plataformas de hosting en la nube.

---

## Características Principales

- **Preguntas en Tiempo Real:** Obtiene preguntas de opción múltiple de *The Trivia API* de forma automática.
- **Modo Respaldo (Fallback):** Si la API externa falla o no responde, el bot carga automáticamente preguntas desde un archivo local (`questions.json`).
- **Botones Interactivos:** Utiliza componentes nativos de Discord UI para seleccionar respuestas mediante botones.
- **Servidor Web e Interfaz (Flask):** Servidor HTTP integrado para monitoreo, landing page y soporte de *keep-alive* para despliegue 24/7 en Render.
- **Control de Acceso y Tiempo:** Cada pregunta está asignada únicamente al usuario que ejecutó el comando y expira automáticamente tras un tiempo límite.
- **Integración con GIPHY:** Muestra GIFs animados interactivos según los aciertos o desaciertos del jugador.
- **Sistema de Puntuación y Ranking:** Registra puntos, aciertos totales y precisión de cada usuario de forma persistente en `scores.json`.
- **Estructura Modular:** Organizado mediante *Cogs*, servicios independientes y plantillas para facilitar el mantenimiento y escalabilidad del código.

---

## Estructura del Proyecto

```text
├── assets/          # Recursos gráficos e imágenes del bot/web
├── cogs/            # Cogs con la lógica de comandos y eventos de Discord
├── services/        # Clientes e integraciones de APIs (Trivia, GIPHY)
├── templates/       # Plantillas HTML para el servidor web Flask
├── utils/           # Funciones auxiliares y utilidades
├── .gitignore       # Archivos omitidos en el repositorio
├── main.py          # Punto de entrada principal (Inicializa Flask y el Bot)
├── questions.json   # Base de datos local de preguntas de respaldo
├── README.md        # Documentación del proyecto
├── requirements.txt # Dependencias de Python
└── scores.json      # Almacenamiento persistente de puntuaciones