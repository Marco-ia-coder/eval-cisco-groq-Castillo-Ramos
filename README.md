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

## Ejemplos de Uso
- **Escenario A:** Entrada: VLAN 10, GESTION, Fa0/1-5 -> Salida: Comandos `vlan 10`, `name GESTION`, etc.
- **Escenario B:** Entrada: OSPF 1, 10.0.0.0 0.0.0.255 area 0 -> Salida: `router ospf 1`, `network...`
- **Escenario C:** Entrada: 192.168.1.0/24, 2 subredes -> Salida: Cálculo de IPs y asignación a Gi0/0 y Gi0/1.

## Limitaciones Conocidas
- Requiere conexión activa a internet para contactar la API de Groq.
- El modelo `llama-3.1-8b-instant` tiene un límite de velocidad (Rate Limit) según el nivel de cuenta del usuario.

## 🎁 Bonificaciones Implementadas
- **Escenario Libre (+3 pts):** Se añadió el **Escenario D (ACLs)** para permitir la creación de filtros de tráfico de red.
- **Modo Conversacional (+2 pts):** El programa ahora mantiene un historial de chat. Después de generar una configuración, el usuario puede pedir ajustes (ej: "cambia la interfaz") y la IA responderá manteniendo el contexto previo.

👤 Autor
Marco Castillo Ramos - Estudiante de Ingeniería - 2026
