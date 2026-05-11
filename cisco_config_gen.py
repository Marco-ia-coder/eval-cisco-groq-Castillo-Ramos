import os
import sys
from datetime import datetime
from groq import Groq

# Parámetros obligatorios de la rúbrica
MODELO_GROQ = "llama-3.1-8b-instant" 
TEMP = 0.2                           
MAX_TOKENS = 800                     

# Historial para el modo conversacional (Bonificación +2)
historial_chat = []

def guardar_configuracion(texto, tipo_escenario):
    if not os.path.exists("configs"):
        os.makedirs("configs")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"configs/escenario_{tipo_escenario}_{timestamp}.txt"
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(texto)
    print(f"\n[+] Configuración guardada en: {nombre_archivo}")

def generar_con_historial(prompt_usuario, tipo_escenario):
    """Implementa el modo conversacional manteniendo el contexto."""
    global historial_chat
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("\n[!] ERROR: Variable GROQ_API_KEY no encontrada.")
        return

    cliente = Groq(api_key=api_key)
    
    # Si es un escenario nuevo, limpiamos el historial
    if tipo_escenario != "REFINE":
        historial_chat = [
            {"role": "system", "content": "Eres un ingeniero experto en Cisco IOS. Genera solo comandos puros. Sin explicaciones."}
        ]
    
    historial_chat.append({"role": "user", "content": prompt_usuario})

    try:
        stream = cliente.chat.completions.create(
            model=MODELO_GROQ,
            messages=historial_chat,
            temperature=TEMP,
            max_tokens=MAX_TOKENS,
            stream=True
        )
        
        texto_completo = ""
        print("\n--- Salida de Configuración ---")
        for chunk in stream:
            if chunk.choices[0].delta.content:
                pedazo = chunk.choices[0].delta.content
                print(pedazo, end="")
                texto_completo += pedazo
        
        historial_chat.append({"role": "assistant", "content": texto_completo})
        guardar_configuracion(texto_completo, tipo_escenario)
        
        # Opción para refinar (Modo Conversacional)
        refinar = input("\n¿Deseas refinar o cambiar algo de esta salida? (s/n): ").lower()
        if refinar == 's':
            cambio = input("¿Qué cambio deseas realizar?: ")
            generar_con_historial(cambio, "REFINE")

    except Exception as e:
        print(f"\n[ERROR] {e}")

def escenario_a_vlans():
    v_id = input("ID VLAN (1-4094): ").strip()
    if not v_id.isdigit() or not (1 <= int(v_id) <= 4094): return
    nom = input("Nombre: ")
    pto = input("Puertos (ej. Fa0/1-5): ")
    prompt = f"Configura VLAN {v_id} llamada {nom}, puertos {pto} acceso, Gi0/1 trunk."
    generar_con_historial(prompt, "A")

def escenario_b_ospf():
    pid = input("ID OSPF (1-65535): ").strip()
    if not pid.isdigit() or not (1 <= int(pid) <= 65535): return
    red = input("Red y Area (ej. 10.0.0.0 0.0.0.255 area 0): ")
    prompt = f"Router OSPF {pid}, network {red}."
    generar_con_historial(prompt, "B")

def escenario_c_subnetting():
    red = input("Red base: ")
    pref = input("Prefijo (8-30): ")
    if not pref.isdigit() or not (8 <= int(pref) <= 30): return
    subs = input("Cant. Subredes: ")
    prompt = f"Subnetting de {red}/{pref} para {subs} subredes. IPs en Gi0/0 y Gi0/1."
    generar_con_historial(prompt, "C")

def escenario_d_acls():
    """Escenario Libre Adicional (Bonificación +3)"""
    print("\n--- Escenario D: ACLs Estándar/Extendidas ---")
    tipo = input("Tipo (estandar/extendida): ").strip().lower()
    nro = input("Número de ACL (1-199): ")
    accion = input("Acción (permit/deny): ")
    origen = input("Origen (ej. 192.168.1.0 0.0.0.255): ")
    prompt = f"Genera una ACL {tipo} número {nro} que haga {accion} al origen {origen}."
    generar_con_historial(prompt, "D")

def main():
    while True:
        print("\n" + "="*30 + "\n GENERADOR PRO - GROQ \n" + "="*30)
        print("1. VLANs\n2. OSPF\n3. Subnetting\n4. ACLs (BONUS)\n0. Salir")
        op = input("\nOpción: ")
        if op == "1": escenario_a_vlans()
        elif op == "2": escenario_b_ospf()
        elif op == "3": escenario_c_subnetting()
        elif op == "4": escenario_d_acls()
        elif op == "0": sys.exit()

if __name__ == "__main__":
    main()