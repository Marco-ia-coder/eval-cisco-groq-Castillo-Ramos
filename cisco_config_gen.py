import os
import sys
from datetime import datetime
from groq import Groq

# Parámetros obligatorios de la rúbrica
MODELO_GROQ = "llama-3.1-8b-instant"
TEMP = 0.2         # Configuración determinística (<= 0.2)
MAX_TOKENS = 800   # (>= 800)

def guardar_configuracion(texto, tipo_escenario):
    """Guarda la salida en la carpeta /configs/ con timestamp."""
    # Verificamos si la carpeta existe, si no, la creamos
    if not os.path.exists("configs"):
        os.makedirs("configs")
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"configs/escenario_{tipo_escenario}_{timestamp}.txt"
    
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(texto)
    print(f"\n[+] Configuración guardada exitosamente en: {nombre_archivo}")

def generar_cisco_ios(prompt_usuario, tipo_escenario):
    """Se conecta a Groq, maneja el streaming y captura errores."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("\n[ERROR CRÍTICO] La variable de entorno GROQ_API_KEY no está configurada.")
        print("Recuerda inyectarla en la consola con: $env:GROQ_API_KEY='tu_clave'")
        sys.exit(1)

    client = Groq(api_key=api_key)

    # System prompt especializado y restrictivo
    system_prompt = """Eres un experto generador de configuraciones Cisco IOS. 
Tu ÚNICA tarea es devolver comandos Cisco IOS sintácticamente válidos en formato de bloque. 
NO incluyas explicaciones, NO saludes, NO uses formato markdown fuera del bloque de código.
Cualquier comentario explicativo debe usar estrictamente el formato de Cisco IOS iniciando la línea con el símbolo '!'.
"""

    print("\nGenerando configuración en tiempo real...\n" + "="*50)
    config_generada = ""

    try:
        # Llamada a la API con stream=True
        stream = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt_usuario}
            ],
            model=MODELO_GROQ,
            temperature=TEMP,
            max_tokens=MAX_TOKENS,
            stream=True
        )

        # Imprimimos los "chunks" (pedacitos) a medida que llegan
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                texto = chunk.choices[0].delta.content
                print(texto, end="", flush=True)
                config_generada += texto
                
        print("\n" + "="*50)
        guardar_configuracion(config_generada, tipo_escenario)

    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg:
            print("\n[ERROR HTTP 429] Rate Limit: Has excedido la cuota de la API de Groq. Espera un momento.")
        elif "Connection" in error_msg or "Network" in error_msg:
            print(f"\n[ERROR DE RED] No se pudo conectar a los servidores de Groq. Revisa tu internet: {e}")
        else:
            print(f"\n[ERROR DE API] Ocurrió un fallo inesperado: {e}")

def escenario_a_vlans():
    """Escenario A: Configuración de VLANs y Trunking con validación."""
    print("\n--- Escenario A: VLANs y Trunking ---")
    vlan_id = input("Ingresa el ID de la VLAN (1-4094): ").strip()

    # VALIDACIÓN: Antes de gastar cuota, verificamos que sea un número válido
    if not vlan_id.isdigit() or not (1 <= int(vlan_id) <= 4094):
        print("\n[!] ERROR: El ID de la VLAN debe ser un número entero entre 1 y 4094.")
        print("Operación cancelada. No se consumió cuota de la API.")
        return

    nombre_vlan = input("Ingresa el nombre de la VLAN (ej. GESTION): ").strip()
    puertos = input("Ingresa los puertos a asignar (ej. FastEthernet0/1 - 5): ").strip()

    prompt = f"Genera la configuración Cisco IOS para crear la VLAN {vlan_id} llamada {nombre_vlan}. Asígnale los puertos {puertos} en modo acceso (switchport mode access). Además, configura el puerto GigabitEthernet0/1 en modo trunk (dot1q) permitiendo esta VLAN."

    generar_cisco_ios(prompt, "A")

def main():
    while True:
        print("\n" + "*"*40)
        print(" GENERADOR INTELIGENTE CISCO IOS - GROQ ")
        print("*"*40)
        print("1. Escenario A: VLANs y Trunking")
        print("2. Escenario B: OSPF (En construcción)")
        print("3. Escenario C: Subnetting (En construcción)")
        print("0. Salir")
        
        opcion = input("\nSelecciona una opción: ").strip()
        
        if opcion == "1":
            escenario_a_vlans()
        elif opcion == "2":
            print("\n[En desarrollo... pasemos a la siguiente etapa luego]")
        elif opcion == "3":
            print("\n[En desarrollo... pasemos a la siguiente etapa luego]")
        elif opcion == "0":
            print("Saliendo del generador...")
            break
        else:
            print("\n[!] Opción no válida.")

if __name__ == "__main__":
    main()