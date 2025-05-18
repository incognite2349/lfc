# analizador-ll1 Project

Este proyecto implementa un analizador LL(1) para gramáticas libres de contexto. Proporciona funciones para calcular los conjuntos First y Follow, realizar análisis descendente y generar tablas LL(1).

## Estructura del Proyecto

```
analizador-ll1
├── src
│   ├── Analisis_descendente.py  # Contiene las funciones principales para el análisis LL(1)
│   ├── interfaz.py               # Implementa la interfaz de usuario para interactuar con el analizador
│   └── utils.py                  # Funciones auxiliares para la lectura de gramáticas y validación
├── requirements.txt               # Lista de dependencias necesarias
└── README.md                      # Documentación del proyecto
```

## Instalación

1. Clona el repositorio:
   ```
   git clone <URL_DEL_REPOSITORIO>
   cd analizador-ll1
   ```

2. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

## Uso

Para utilizar el analizador, ejecuta el archivo `interfaz.py`:

```
python src/interfaz.py
```

La interfaz te permitirá:

- Calcular los conjuntos First y Follow.
- Realizar el análisis descendente de una palabra.
- Generar la tabla LL(1) para una gramática dada.

## Ejemplos

1. **Calcular First**:
   - Ingresa la gramática y selecciona la opción para calcular el conjunto First.

2. **Calcular Follow**:
   - Ingresa la gramática y selecciona la opción para calcular el conjunto Follow.

3. **Análisis Descendente**:
   - Proporciona una palabra y la gramática para realizar el análisis.

4. **Generar Tabla LL(1)**:
   - Ingresa la gramática para obtener la tabla LL(1).

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir, por favor abre un issue o un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT.