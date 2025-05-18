def leer_gramatica(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        cantidad_gramaticas = int(file.readline().strip())
        todas_gramaticas = []

        for _ in range(cantidad_gramaticas):
            cantidad_no_terminales = int(file.readline().strip())
            gramatica = {}
            no_terminales_definidos = set()

            for _ in range(cantidad_no_terminales):
                linea = file.readline().strip().split()
                no_terminal = linea[0]
                producciones = linea[1:]

                if not no_terminal.isupper():
                    print(f"Error: El no terminal '{no_terminal}' no está en mayúsculas.")
                    return None

                for produccion in producciones:
                    if "e" in produccion or "$" in produccion:
                        print(f"Error: La producción '{produccion}' contiene 'e' o '$', lo cual no está permitido.")
                        return None

                no_terminales_definidos.add(no_terminal)
                gramatica[no_terminal] = producciones

            for no_terminal, producciones in gramatica.items():
                for produccion in producciones:
                    for simbolo in produccion:
                        if simbolo.isupper() and simbolo not in no_terminales_definidos:
                            print(f"Error: El no terminal '{simbolo}' en la producción de '{no_terminal}' no está definido.")
                            return None

            todas_gramaticas.append(gramatica)

        return todas_gramaticas

def validar_entrada(entrada):
    if not entrada:
        print("Error: La entrada no puede estar vacía.")
        return False
    return True

def mostrar_mensaje(mensaje):
    print(mensaje)