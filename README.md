# Generador Inteligente de Configuraciones Cisco IOS 🚀

Este proyecto es una herramienta de automatización basada en Python que utiliza la API de **Groq** (modelo Llama 3.1) para generar configuraciones de red precisas para dispositivos Cisco IOS. El sistema permite a los administradores de red obtener comandos listos para usar en escenarios de VLANs, enrutamiento OSPF y direccionamiento IP (Subnetting).

## 🛠️ Características
- **Generación en tiempo real:** Uso de streaming para visualizar la salida de la IA al instante.
- **Persistencia de datos:** Todas las configuraciones se guardan automáticamente en archivos `.txt` con marca de tiempo en la carpeta `/configs/`.
- **Validación de entrada:** Filtros robustos para asegurar que los IDs de VLAN, procesos OSPF y prefijos de red sean válidos antes de consultar la API.
- **Seguridad:** Manejo de credenciales mediante variables de entorno.

## 📋 Requisitos
- Python 3.10 o superior.
- Una API Key de [Groq Cloud](https://console.groq.com/).
- Las librerías listadas en `requirements.txt`.

## 🚀 Instalación y Uso

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/tu-usuario/eval-cisco-groq-Castillo-Ramos.git](https://github.com/tu-usuario/eval-cisco-groq-Castillo-Ramos.git)
   cd eval-cisco-groq-Castillo-Ramos

2- Configurar el entorno virtual:
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

3- Configurar la API Key:
$env:GROQ_API_KEY="tu_api_key_aqui"

4- Ejecutar el programa:
python cisco_config_gen.py

## Justificación de Parámetros de IA
- **Temperature (0.2):** Se seleccionó un valor bajo para garantizar respuestas precisas y determinísticas, evitando alucinaciones en los comandos de configuración.
- **Max Tokens (800):** Se estableció este límite para asegurar que las configuraciones complejas (especialmente en subnetting) se entreguen completas sin cortes abruptos.

👤 Autor
Marco Castillo Ramos - Estudiante de Ingeniería - 2026
