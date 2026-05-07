import os
import sys
from datetime import datetime
from groq import Groq

# Parámetros obligatorios de la rúbrica
MODELO_GROQ = "llama-3.1-8b-instant" 
TEMP = 0.2                           
MAX_TOKENS = 800                     

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
        print("\n[!] ERROR: ID de VLAN inválido.")
        return
        
    nombre = input("Ingresa el nombre de la VLAN: ").strip()
    puertos = input("Ingresa los puertos (ej. Fa0/1 - 10): ").strip()
    
    prompt = f"Crea la VLAN {vlan_id} con el nombre {nombre}. Asigna los puertos {puertos} en modo acceso. Configura Gi0/1 en modo trunk para la VLAN {vlan_id}."
    generar_cisco_ios(prompt, "A")

def escenario_b_ospf():
    print("\n--- Escenario B: Enrutamiento OSPF ---")
    proceso_id = input("Ingresa el ID del proceso OSPF (1-65535): ").strip()

    if not proceso_id.isdigit() or not (1 <= int(proceso_id) <= 65535):
        print("\n[!] ERROR: ID de proceso OSPF inválido.")
        return

    redes = input("Ingresa redes (ej. 192.168.1.0 0.0.0.255 area 0): ").strip()
    prompt = f"Configura OSPF proceso {proceso_id}. Anuncia las redes: {redes}. Solo comandos Cisco IOS."
    generar_cisco_ios(prompt, "B")

def escenario_c_subnetting():
    print("\n--- Escenario C: Subnetting e Interfaces ---")
    red_base = input("Ingresa la red base (ej. 192.168.10.0): ").strip()
    prefijo = input("Ingresa el prefijo (8-30): ").strip()

    if not prefijo.isdigit() or not (8 <= int(prefijo) <= 30):
        print("\n[!] ERROR: El prefijo debe estar entre 8 y 30.")
        return

    subredes = input("Cantidad de subredes requeridas: ").strip()
    prompt = f"Realiza subnetting de {red_base}/{prefijo} para {subredes} subredes. Genera comandos para asignar la primera IP utilizable de la Subred 1 a Gi0/0 y la primera IP de la Subred 2 a Gi0/1. Incluye no shutdown."
    generar_cisco_ios(prompt, "C")

def main():
    while True:
        print("\n****************************************")
        print("  GENERADOR INTELIGENTE CISCO IOS - GROQ")
        print("****************************************")
        print("1. Escenario A: VLANs y Trunking")
        print("2. Escenario B: OSPF")
        print("3. Escenario C: Subnetting e Interfaces")
        print("0. Salir")

        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "1":
            escenario_a_vlans()
        elif opcion == "2":
            escenario_b_ospf()
        elif opcion == "3":
            escenario_c_subnetting()
        elif opcion == "0":
            print("Saliendo...")
            sys.exit()
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()