import numpy as np

from constantes import Texts
from transformaciones import Transformacion

# Asegúrate de haber definido correctamente la clase Transformacion, que debe calcular
# matriz_transformacion y matriz_inversa en coordenadas homogéneas (3x3)


def prueba_transformaciones():
    # Definimos algunos puntos como columnas, en coordenadas homogéneas (3x4)
    puntos_iniciales = np.array(
        [
            [1, 3, 3, 1],  # Coordenadas x de cada punto
            [1, 1, 3, 3],  # Coordenadas y de cada punto
            [1, 1, 1, 1],  # Para mantener homogéneo el vector
        ]
    )

    # Definimos algunas transformaciones para probar
    transformaciones = {
        Texts.TRANS_TRASLACION: (0, 0),  # Traslación de +2 en x y +3 en y
        Texts.TRANS_ESCALADO: (1, 1),  # Escala de 1.5x en x y 0.5x en y
        Texts.TRANS_ROTACION: (0, True),  # Rotación de 45 grados en sentido horario
        Texts.TRANS_SHEARING: (0, 0),  # Shearing de 0.2 en x y 0.3 en y
        Texts.TRANS_REFLEXION: (Texts.REFLEXION_LINE, 3, 2),  # Reflexión en el origen
    }

    # Crear la instancia de transformación
    transformacion = Transformacion(transformaciones)

    # Aplicar la transformación a los puntos
    puntos_transformados = transformacion.transformar(puntos_iniciales)
    puntos_revertidos = transformacion.deshacer_transformacion(puntos_transformados)

    # Mostrar los resultados
    print("Puntos iniciales:\n", puntos_iniciales)
    print("\nMatriz de transformación:\n", transformacion.matriz_transformacion)
    print("\nPuntos después de la transformación:\n", puntos_transformados)
    print("\nMatriz inversa de la transformación:\n", transformacion.matriz_inversa)
    print("\nPuntos después de revertir la transformación:\n", puntos_revertidos)


# Ejecuta la prueba
prueba_transformaciones()
