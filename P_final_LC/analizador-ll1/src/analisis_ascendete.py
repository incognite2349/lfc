from utils import leer_gramatica
from Analisis_descendente import calcular_first, calcular_follow

def closure(items, gramatica):
    closure_set = set(items)
    added = True
    while added:
        added = False
        new_items = set()
        for (head, body, dot_pos) in closure_set:
            if dot_pos < len(body):
                symbol = body[dot_pos]
                if symbol in gramatica:  # Es un no terminal
                    for prod in gramatica[symbol]:
                        item = (symbol, prod, 0)
                        if item not in closure_set:
                            new_items.add(item)
        if new_items:
            closure_set.update(new_items)
            added = True
    return closure_set

def goto(items, symbol, gramatica):
    moved = set()
    for (head, body, dot_pos) in items:
        if dot_pos < len(body) and body[dot_pos] == symbol:
            moved.add((head, body, dot_pos + 1))
    return closure(moved, gramatica)

def construir_automata_lr0(gramatica):
    # Paso 1: producción aumentada
    simbolo_inicial = next(iter(gramatica))
    gramatica_aumentada = {"S'": [simbolo_inicial], **gramatica}
    # Paso 2: estado inicial
    estado_inicial = closure({("S'", gramatica_aumentada["S'"][0], 0)}, gramatica_aumentada)
    estados = [estado_inicial]
    transiciones = []
    visitados = [estado_inicial]
    while visitados:
        actual = visitados.pop()
        simbolos = set()
        for (head, body, dot_pos) in actual:
            if dot_pos < len(body):
                simbolos.add(body[dot_pos])
        for simbolo in simbolos:
            siguiente = goto(actual, simbolo, gramatica_aumentada)
            if siguiente and siguiente not in estados:
                estados.append(siguiente)
                visitados.append(siguiente)
            if siguiente:
                transiciones.append((actual, simbolo, siguiente))
    return estados, transiciones

def construir_tabla_slr(gramatica, first, follow):
    # Construir el autómata LR(0)
    estados, transiciones = construir_automata_lr0(gramatica)
    simbolo_inicial = next(iter(gramatica))
    gramatica_aumentada = {"S'": [simbolo_inicial], **gramatica}
    terminales = set()
    no_terminales = set(gramatica.keys())

    # Obtener terminales
    for producciones in gramatica.values():
        for prod in producciones:
            for simbolo in prod:
                if not simbolo.isupper() and simbolo != "ε":
                    terminales.add(simbolo)
    terminales.add("$")

    # Inicializar tabla
    tabla = [{} for _ in range(len(estados))]

    # Mapear estados a índices
    estado_indices = {frozenset(e): i for i, e in enumerate(estados)}

    # Llenar la tabla
    for i, estado in enumerate(estados):
        for (head, body, dot_pos) in estado:
            # SHIFT
            if dot_pos < len(body):
                simbolo = body[dot_pos]
                siguiente = goto(estado, simbolo, gramatica_aumentada)
                if siguiente in estados:
                    j = estado_indices[frozenset(siguiente)]
                    if simbolo in terminales:
                        tabla[i][simbolo] = f"s{j}"  # shift
                    elif simbolo in no_terminales:
                        tabla[i][simbolo] = j        # goto
            # REDUCE o ACCEPT
            else:
                if head == "S'":
                    tabla[i]["$"] = "acc"
                else:
                    for t in follow[head]:
                        prod_num = None
                        # Buscar el número de producción
                        for idx, prod in enumerate(gramatica[head]):
                            if prod == body:
                                prod_num = (head, prod)
                                break
                        if prod_num is not None:
                            tabla[i][t] = f"r{head}->{body}"

    return tabla

def analizar_palabra_slr(palabra, tabla_slr, simbolo_inicial):
    # Convertir la palabra en una lista de símbolos y agregar el fin de cadena
    entrada = list(palabra) + ["$"]
    pila = [0]  # La pila comienza con el estado 0
    salida = [] # Para registrar los pasos

    idx = 0
    while True:
        estado = pila[-1]
        simbolo = entrada[idx]
        accion = tabla_slr[estado].get(simbolo, "")

        salida.append(f"Pila: {pila} | Entrada: {entrada[idx:]} | Acción: {accion}")

        if accion == "":
            salida.append("Error de sintaxis.")
            break
        elif accion == "acc":
            salida.append("Cadena aceptada.")
            break
        elif accion.startswith("s"):  # Shift
            nuevo_estado = int(accion[1:])
            pila.append(simbolo)
            pila.append(nuevo_estado)
            idx += 1
        elif accion.startswith("r"):  # Reduce
            # Extraer la producción
            produccion = accion[1:]
            head, body = produccion.split("->")
            head = head.strip()
            body = body.strip()
            if body == "ε":
                body_len = 0
            else:
                body_len = len(body)
            # Sacar 2*body_len elementos de la pila (símbolo y estado por cada símbolo)
            for _ in range(2 * body_len):
                pila.pop()
            estado_actual = pila[-1]
            pila.append(head)
            goto_estado = tabla_slr[estado_actual].get(head)
            if goto_estado is None:
                salida.append("Error: transición goto no encontrada.")
                break
            pila.append(goto_estado)
        else:
            salida.append("Acción desconocida.")
            break

    return "\n".join(salida)

def imprimir_tabla_slr(tabla_slr):
    # Obtener todos los símbolos usados en la tabla
    simbolos = set()
    for fila in tabla_slr:
        simbolos.update(fila.keys())
    simbolos = sorted(simbolos)

    # Imprimir encabezado
    encabezado = "Estado".ljust(8) + "".join(s.ljust(12) for s in simbolos)
    print(encabezado)
    print("-" * len(encabezado))

    # Imprimir cada fila de la tabla
    for i, fila in enumerate(tabla_slr):
        linea = str(i).ljust(8)
        for s in simbolos:
            accion = fila.get(s, "")
            linea += accion.ljust(12)
        print(linea)