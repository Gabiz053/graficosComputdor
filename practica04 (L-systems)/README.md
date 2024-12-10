# L-System Viewer

Este proyecto es una interfaz gráfica desarrollada con **CustomTkinter** que permite explorar ejemplos de sistemas L (L-Systems) y generar dibujos basados en reglas definidas.

## Características

- Selección de ejemplos predefinidos de L-Systems.
- Configuración personalizada de:
  - Iteraciones
  - Velocidad del dibujo
  - Longitud de los segmentos
- Habilitar o deshabilitar el dibujo instantáneo.
- Generación de dibujos con colores y patrones personalizados.

## Requisitos

- Python 3.12 o superior.
- Bibliotecas requeridas:
  - [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
  - Turtle (incluida en Python estándar).

## Instalación

2. Instala las dependencias requeridas:

   ```bash
   pip install customtkinter
   pip install turtle
   ```

3. Ejecuta la aplicación:

   ```bash
   python veentana.py
   ```

## Uso

1. Selecciona un ejemplo de L-System desde el desplegable.
2. Configura los parámetros:
   - **Iteraciones**: Número de iteraciones para generar el patrón.
   - **Velocidad**: Velocidad del dibujo.
   - **Longitud**: Longitud de los segmentos.
   - **Dibujo instantáneo**: Habilita o deshabilita esta opción.
3. Haz clic en el botón **Generar** para visualizar el L-System.

## Estructura del Proyecto

- `ventana.py`: Archivo principal que contiene la clase `Ventana`.
- `ejemplos.py`: Define los axiomas, reglas y configuraciones de los L-Systems predefinidos.
- `LSystem.py`: Contiene la implementación del generador y dibujador de L-Systems.

## Personalización

### Agregar un Nuevo Ejemplo de L-System

1. Ve al archivo `ejemplos.py`.

2. Añade un nuevo diccionario al conjunto de ejemplos con la siguiente estructura:

   ```python
   {
       "nombre_del_ejemplo": {
           "axioma": "F",
           "reglas": {"F": "F+F--F+F"},
           "angulo": 60,
           "punto_inicial": (0, 0),
           "rotacion": 0,
           "colormap": "cool",
       }
   }
   ```

3. Actualiza `OPCIONES` con el nombre del nuevo ejemplo.

## Acerca del Autor

- **Gabriel Gómez García** - [GitHub](https://github.com/Gabiz053)

## Fuentes y Agradecimientos

Este proyecto se benefició de valiosas contribuciones y recursos:

- La comunidad de [Tkinter](https://wiki.python.org/moin/TkInter), por su documentación exhaustiva y ejemplos prácticos.
- [StackOverflow](https://stackoverflow.com/), por el apoyo colaborativo en la resolución de desafíos técnicos.
- La [documentación oficial de Python](https://docs.python.org/3/), una fuente confiable para el lenguaje y sus módulos estándar.

