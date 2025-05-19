from utils import *


def calcular_first(gramatica):
    first = {
        no_terminal: set() for no_terminal in gramatica
    }

    for producciones in gramatica.values():
        for produccion in producciones:
            for simbolo in produccion:
                if not simbolo.isupper() and simbolo not in first:
                    first[simbolo] = {simbolo}

    def obtener_first(no_terminal, visitados):
        if no_terminal in visitados:
            return set()

        visitados.add(no_terminal)

        for produccion in gramatica[no_terminal]:
            primer_simbolo = produccion[0]

            if not primer_simbolo.isupper():
                first[no_terminal].add(primer_simbolo)
            else:
                first[no_terminal].update(obtener_first(primer_simbolo, visitados))

        visitados.remove(no_terminal)
        return first[no_terminal]

    for no_terminal in gramatica:
        obtener_first(no_terminal, set())

    return first


def calcular_follow(gramatica, first):
    follow = {
        no_terminal: set() for no_terminal in gramatica
    }
    follow[next(iter(gramatica))].add("$")

    def agregar_follow(no_terminal):
        for nt, producciones in gramatica.items():
            for produccion in producciones:
                for i in range(len(produccion)):
                    if produccion[i] == no_terminal:
                        if i < len(produccion) - 1:
                            siguiente = produccion[i + 1]
                            if siguiente.isupper():
                                follow[no_terminal].update(first[siguiente] - {"ε"})
                                if "ε" in first[siguiente]:
                                    follow[no_terminal].update(follow[nt])
                            else:
                                follow[no_terminal].add(siguiente)

                        if i == len(produccion) - 1:
                            follow[no_terminal].update(follow[nt])

    for no_terminal in gramatica:
        agregar_follow(no_terminal)

    return follow


def obtener_first_produccion(produccion, first):
    result = set()
    for simbolo in produccion:
        if simbolo in first:
            result.update(first[simbolo] - {"ε"})
            if "ε" not in first[simbolo]:
                break
        else:
            result.add(simbolo)
            break
    else:
        result.add("ε")  # Usar "ε" en vez de ""
    return result


def es_ll1(gramatica):
    first = calcular_first(gramatica)
    follow = calcular_follow(gramatica, first)

    for no_terminal, producciones in gramatica.items():
        for i in range(len(producciones)):
            for j in range(i + 1, len(producciones)):
                first_i = obtener_first_produccion(producciones[i], first)
                first_j = obtener_first_produccion(producciones[j], first)

                if first_i & first_j:
                    return False

                if "" in first_i:
                    if first_j & follow[no_terminal]:
                        return False
                if "" in first_j:
                    if first_i & follow[no_terminal]:
                        return False

    return True


def construir_tabla_ll1(gramatica, first, follow):
    terminales = set()
    for producciones in gramatica.values():
        for produccion in producciones:
            for simbolo in produccion:
                if not simbolo.isupper() and simbolo != "ε":
                    terminales.add(simbolo)
    terminales.add("$")

    no_terminales = list(gramatica.keys())

    matriz = {
        no_terminal: {terminal: "" for terminal in terminales}
        for no_terminal in no_terminales
    }

    for no_terminal, producciones in gramatica.items():
        for produccion in producciones:
            first_produccion = obtener_first_produccion(produccion, first)

            for terminal in first_produccion:
                if terminal != "ε":
                    matriz[no_terminal][terminal] = f"{no_terminal} -> {produccion}"

            if "ε" in first_produccion:
                for terminal in follow[no_terminal]:
                    matriz[no_terminal][terminal] = f"{no_terminal} -> {produccion}"

    return matriz


def imprimir_matriz_ll1(matriz):
    terminales = list(next(iter(matriz.values())).keys())
    no_terminales = list(matriz.keys())

    print("         " + "            ".join(terminales))
    print("  +" + "------------+" * len(terminales))

    for no_terminal in no_terminales:
        fila = [matriz[no_terminal][terminal] for terminal in terminales]
        print(f"{no_terminal} | " + " | ".join(f"{celda:10}" for celda in fila) + " |")
        print("  +" + "------------+" * len(terminales))


def analizar_palabra(palabra, matriz_ll1, simbolo_inicial):
    pila = [
        "$",
        simbolo_inicial,
    ]
    entrada = list(palabra) + ["$"]
    pasos = []

    while pila:
        cima = pila[-1]
        simbolo_entrada = entrada[0]

        if cima == simbolo_entrada:
            pila.pop()
            entrada.pop(0)
            pasos.append((cima, "".join(pila), "".join(entrada), "Coincide"))
        elif cima in matriz_ll1 and simbolo_entrada in matriz_ll1[cima]:
            produccion = matriz_ll1[cima][simbolo_entrada]
            if produccion:
                produccion_simbolos = produccion.split("->")[1].strip()
                if produccion_simbolos != "ε":
                    pila.pop()
                    pila.extend(
                        reversed(produccion_simbolos)
                    )
                else:
                    pila.pop()
                pasos.append((cima, "".join(pila), "".join(entrada), produccion))

            else:
                pasos.append(
                    (cima, "".join(pila), "".join(entrada), "Error: No hay producción")
                )
                break
        else:
            pasos.append(
                (cima, "".join(pila), "".join(entrada), "Error: No hay producción")
            )
            break

    return pasos


def imprimir_pasos(pasos):
    print(f"{'Cima':<10} {'Pila':<20} {'Entrada':<20} {'Acción':<30}")
    print("=" * 80)
    for paso in pasos:
        cima, pila, entrada, accion = paso
        # Mejora visual con emojis
        if "aceptada" in accion.lower():
            accion = "✅ " + accion
        elif "error" in accion.lower():
            accion = "❌ " + accion
        elif "Coincide" in accion:
            accion = "📥 " + accion
        print(f"{cima:<10} {pila:<20} {entrada:<20} {accion:<30}")