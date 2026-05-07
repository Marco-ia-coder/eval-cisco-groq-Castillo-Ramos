import os
import sys
from datetime import datetime
from groq import Groq

# Parámetros obligatorios de la rúbrica
MODELO_GROQ = "llama-3.1-8b-instant" # Modelo actualizado
TEMP = 0.2                           # Configuración determinística (<= 0.2)
MAX_TOKENS = 800                     # (>= 800)

def guardar_configuracion(texto, tipo_escenario):
    """Guarda la salida en la carpeta /configs/ con timestamp."""
    if not os.path.exists("configs"):
        os.makedirs("configs")
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"configs/escenario_{tipo_escenario}_{timestamp}.txt"
    
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(texto)
    print(f"\n[+] Configuración guardada exitosamente en: {nombre_archivo}")

def generar_cisco_ios(prompt_especifico, tipo_escenario):
    """Se comunica con Groq, imprime en streaming y guarda el archivo."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("\n[!] ERROR: Variable de entorno GROQ_API_KEY no encontrada.")
        return

    cliente = Groq(api_key=api_key)
    system_prompt = "Eres un ingeniero experto en Cisco IOS. Genera solo los comandos de configuración solicitados. No incluyas explicaciones, markdown, ni saludos. Solo entrega código puro en formato bloque."

    print("\nGenerando configuración en tiempo real...")
    print("========================================\n")

    try:
        stream = cliente.chat.completions.create(
            model=MODELO_GROQ,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt_especifico}
            ],
            temperature=TEMP,
            max_tokens=MAX_TOKENS,
            stream=True
        )

        texto_completo = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                pedazo = chunk.choices[0].delta.content
                print(pedazo, end="")
                texto_completo += pedazo
                
        print("\n\n========================================")
        guardar_configuracion(texto_completo, tipo_escenario)

    except Exception as e:
        print(f"\n[ERROR DE API] Ocurrió un fallo inesperado: {e}")

def escenario_a_vlans():
    print("\n--- Escenario A: VLANs y Trunking ---")
    vlan_id = input("Ingresa el ID de la VLAN (1-4094): ").strip()
    
    if not vlan_id.isdigit() or not (1 <= int(vlan_id) <= 4094):
        print("\n[!] ERROR: El ID de la VLAN debe ser un número entre 1 y 4094.")
        return
        
    nombre = input("Ingresa el nombre de la VLAN (ej. GESTION): ").strip()
    puertos = input("Ingresa los puertos a asignar (ej. FastEthernet0/1 - 5): ").strip()
    
    prompt = f"Crea la VLAN {vlan_id} con el nombre {nombre}. Asigna los puertos {puertos} en modo acceso a esta VLAN. Configura la interfaz GigabitEthernet0/1 en modo trunk permitiendo pasar la VLAN {vlan_id}. Entregame solo los comandos de Cisco IOS."
    generar_cisco_ios(prompt, "A")

def escenario_b_ospf():
    print("\n--- Escenario B: Enrutamiento OSPF ---")
    proceso_id = input("Ingresa el ID del proceso OSPF (1-65535): ").strip()

    if not proceso_id.isdigit() or not (1 <= int(proceso_id) <= 65535):
        print("\n[!] ERROR: El ID de proceso OSPF debe ser numérico entre 1 y 65535.")
        return

    redes = input("Ingresa las redes a anunciar con su wildcard y área (ej. 192.168.1.0 0.0.0.255 area 0): ").strip()
    prompt = f"Genera la configuración Cisco IOS para un router usando OSPF con el ID de proceso {proceso_id}. Anuncia las siguientes redes estrictamente: {redes}. Entregame solo los comandos."
    generar_cisco_ios(prompt, "B")

def main():
    while True:
        print("\n****************************************")
        print("  GENERADOR INTELIGENTE CISCO IOS - GROQ")
        print("****************************************")
        print("1. Escenario A: VLANs y Trunking")
        print("2. Escenario B: OSPF")
        print("3. Escenario C: Subnetting e Interfaces (En construcción)")
        print("0. Salir")

        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "1":
            escenario_a_vlans()
        elif opcion == "2":
            escenario_b_ospf()
        elif opcion == "3":
            print("\n[!] El Escenario C estará disponible en la próxima actualización.")
        elif opcion == "0":
            print("Saliendo del generador...")
            sys.exit()
        else:
            print("Opción inválida. Intenta nuevamente.")

if __name__ == "__main__":
    main()