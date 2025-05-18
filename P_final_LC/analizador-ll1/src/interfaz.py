from Analisis_descendente import *
from analisis_ascendete import *
import os

ARCHIVO_GRAMATICA = os.path.join(os.path.dirname(__file__), "gramatica.txt")

def main():
    while True:
        print("----------------------")
        print("\nMenú de opciones:")
        print("1. Calcular conjuntos First")
        print("2. Calcular conjuntos Follow")
        print("3. Verificar si la gramática es LL(1)")
        print("4. Construir tabla LL(1)")
        print("5. Analizar palabra")
        print("6. Construir tabla SLR(1)")
        print("7. Analizar palabra (SLR(1))")
        print("8. Salir")
        print("----------------------")

        opcion = input("Seleccione una opción (1-8): ")
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
                if es_ll1(gramatica):
                    print("La gramática es LL(1).")
                else:
                    print("La gramática no es LL(1).")

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
            gramatica_list = leer_gramatica(ARCHIVO_GRAMATICA)
            if gramatica_list:
                gramatica = gramatica_list[0]
                first = calcular_first(gramatica)
                follow = calcular_follow(gramatica, first)
                tabla_ll1 = construir_tabla_ll1(gramatica, first, follow)
                palabra = input("Ingrese la palabra a analizar: ")
                simbolo_inicial = next(iter(gramatica))
                pasos = analizar_palabra(palabra, tabla_ll1, simbolo_inicial)
                imprimir_pasos(pasos)

        elif opcion == "6":
            gramatica_list = leer_gramatica(ARCHIVO_GRAMATICA)
            if gramatica_list:
                gramatica = gramatica_list[0]
                first = calcular_first(gramatica)
                follow = calcular_follow(gramatica, first)
                tabla_slr = construir_tabla_slr(gramatica, first, follow)
                imprimir_tabla_slr(tabla_slr)

        elif opcion == "7":
            gramatica_list = leer_gramatica(ARCHIVO_GRAMATICA)
            if gramatica_list:
                gramatica = gramatica_list[0]
                first = calcular_first(gramatica)
                follow = calcular_follow(gramatica, first)
                tabla_slr = construir_tabla_slr(gramatica, first, follow)
                palabra = input("Ingrese la palabra a analizar: ")
                simbolo_inicial = next(iter(gramatica))
                resultado = analizar_palabra_slr(palabra, tabla_slr, simbolo_inicial)
                print(resultado)

        elif opcion == "8":
            print("Saliendo del programa.")
            break

        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()