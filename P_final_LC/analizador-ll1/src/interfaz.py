from Analisis_descendente import *
from analisis_ascendete import *
import os

ARCHIVO_GRAMATICA = os.path.join(os.path.dirname(__file__), "gramatica.txt")

def main():
    tipo_gramatica = None
    tabla_usada = None
    simbolo_inicial = None

    while True:
        print("----------------------")
        print("\nMenú de opciones:")
        print("1. Calcular conjuntos First")
        print("2. Calcular conjuntos Follow")
        print("3. Verificar si la gramática es LL(1) o SLR(1)")
        print("4. Construir tabla LL(1)")
        print("5. Analizar palabra")
        print("6. Construir tabla SLR(1)")
        print("7. Salir")
        print("----------------------")

        opcion = input("Seleccione una opción (1-7): ")
        print("----------------------")

        if opcion == "1":
            gramatica_list = leer_gramatica(ARCHIVO_GRAMATICA)
            if gramatica_list:
                gramatica = gramatica_list[0]
                first = calcular_first(gramatica)
                print("Conjuntos First:")
                for nt, conjunto in first.items():
                    print(f"{nt}: {conjunto}")

        elif opcion == "2":
            gramatica_list = leer_gramatica(ARCHIVO_GRAMATICA)
            if gramatica_list:
                gramatica = gramatica_list[0]
                first = calcular_first(gramatica)
                follow = calcular_follow(gramatica, first)
                print("Conjuntos Follow:")
                for nt, conjunto in follow.items():
                    print(f"{nt}: {conjunto}")

        elif opcion == "3":
            gramatica_list = leer_gramatica(ARCHIVO_GRAMATICA)
            if gramatica_list:
                gramatica = gramatica_list[0]
                simbolo_inicial = next(iter(gramatica))
                first = calcular_first(gramatica)
                follow = calcular_follow(gramatica, first)
                if es_ll1(gramatica):
                    print("La gramática es LL(1).")
                    tipo_gramatica = "LL1"
                    tabla_usada = construir_tabla_ll1(gramatica, first, follow)
                else:
                    print("La gramática NO es LL(1).")
                    tabla_slr = construir_tabla_slr(gramatica, first, follow)
                    if es_slr1(tabla_slr):
                        print("La gramática es SLR(1).")
                        tipo_gramatica = "SLR1"
                        tabla_usada = tabla_slr
                    else:
                        print("La gramática NO es SLR(1).")
                        tipo_gramatica = None
                        tabla_usada = None

        elif opcion == "4":
            gramatica_list = leer_gramatica(ARCHIVO_GRAMATICA)
            if gramatica_list:
                gramatica = gramatica_list[0]
                first = calcular_first(gramatica)
                follow = calcular_follow(gramatica, first)
                tabla_ll1 = construir_tabla_ll1(gramatica, first, follow)
                print("Tabla LL(1):")
                imprimir_matriz_ll1(tabla_ll1)

        elif opcion == "5":
            if tipo_gramatica is None or tabla_usada is None:
                print("Primero verifique el tipo de gramática con la opción 3.")
            else:
                palabra = input("Ingrese la palabra a analizar: ")
                if tipo_gramatica == "LL1":
                    pasos = analizar_palabra(palabra, tabla_usada, simbolo_inicial)
                    imprimir_pasos(pasos)
                elif tipo_gramatica == "SLR1":
                    resultado = analizar_palabra_slr(palabra, tabla_usada, simbolo_inicial)
                    print(resultado)
                else:
                    print("La gramática no es LL(1) ni SLR(1). No se puede analizar la palabra.")

        elif opcion == "6":
            gramatica_list = leer_gramatica(ARCHIVO_GRAMATICA)
            if gramatica_list:
                gramatica = gramatica_list[0]
                first = calcular_first(gramatica)
                follow = calcular_follow(gramatica, first)
                tabla_slr = construir_tabla_slr(gramatica, first, follow)
                imprimir_tabla_slr(tabla_slr)

        elif opcion == "7":
            print("Saliendo del programa.")
            break

        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()