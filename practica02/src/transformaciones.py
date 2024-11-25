import numpy as np

from constantes import Texts


class Transformacion:
    def __init__(self, transformaciones, puntos_poligono):
        """
        Inicializa la clase Transformacion, creando matrices de transformación e inversa.

        Argumentos:
            transformaciones (dict): Diccionario con parámetros de cada tipo de transformación.
        """
        self._puntos = puntos_poligono
        # calculamos directamente el centro del poligono por si lo usamos
        self.x_center = np.mean(self._puntos[0, :])
        self.y_center = np.mean(self._puntos[1, :])
    
        self.matriz_transformacion, self.matriz_inversa = self._crear_matrices(
            transformaciones
        )
        
        self.transformaciones = transformaciones

    def _crear_matrices(self, transformaciones):
        """
        Genera la matriz de transformación combinada y su inversa, basándose en los parámetros.

        Argumentos:
            transformaciones (dict): Diccionario con parámetros para cada transformación.

        Retorna:
            tuple: Matriz de transformación y matriz inversa.
        """
        # Extraer los parámetros para cada transformación
        x_translation, y_translation = transformaciones.get(
            Texts.TRANS_TRASLACION, (0, 0)
        )
        x_scale, y_scale = transformaciones.get(Texts.TRANS_ESCALADO, (1, 1))

        rotation_angle, rotation_direction = transformaciones.get(
            Texts.TRANS_ROTACION, (0, True)
        )
        shearing_x, shearing_y = transformaciones.get(Texts.TRANS_SHEARING, (0, 0))

        reflexion_modo, pendiente, ordenada = transformaciones.get(
            Texts.TRANS_REFLEXION, (None, None, None)
        )

        # nos aseguramos que tengan el tipo correcto
        x_translation = int(x_translation)
        y_translation = int(y_translation)
        x_scale = float(x_scale)
        y_scale = float(y_scale)
        rotation_angle = float(rotation_angle)
        rotation_direction = bool(rotation_direction)
        shearing_x = float(shearing_x)
        shearing_y = float(shearing_y)

        # Generar las matrices de transformación
        matriz_traslacion, matriz_traslacion_inv = self._traslacion(
            x_translation, y_translation
        )
        matriz_escalado, matriz_escalado_inv = self._escalado(x_scale, y_scale)
        matriz_rotacion, matriz_rotacion_inv = self._rotacion(
            rotation_angle, rotation_direction
        )
        matriz_shearing, matriz_shearing_inv = self._shearing(shearing_x, shearing_y)
        matriz_reflexion, matriz_reflexion_inv = self._reflexion(
            reflexion_modo, pendiente, ordenada
        )

        # Combinación de todas las matrices
        matriz_transformacion = (
            matriz_reflexion
            @ matriz_shearing
            @ matriz_rotacion
            @ matriz_escalado
            @ matriz_traslacion
        )

        # Inversa de la matriz combinada
        matriz_inversa = (
            matriz_traslacion_inv
            @ matriz_escalado_inv
            @ matriz_rotacion_inv
            @ matriz_shearing_inv
            @ matriz_reflexion_inv
        )

        return matriz_transformacion, matriz_inversa

    def _traslacion(self, x_translation, y_translation):
        matriz = np.array([[1, 0, x_translation], [0, 1, y_translation], [0, 0, 1]])
        matriz_inv = np.array(
            [[1, 0, -x_translation], [0, 1, -y_translation], [0, 0, 1]]
        )
        return matriz, matriz_inv

    def _escalado(self, x_scale, y_scale):
        # 1. Mover el centro al origen
        traslacion, traslacion_inv = self._traslacion(
            self.x_center, self.y_center
        )

        # 2. Escalar correctamente
        matriz = np.array([[x_scale, 0, 0], [0, y_scale, 0], [0, 0, 1]])
        matriz_inv = np.array(
            [
                [1 / x_scale if x_scale != 0 else 0, 0, 0],
                [0, 1 / y_scale if y_scale != 0 else 0, 0],
                [0, 0, 1],
            ]
        )
        # 3. multiplicar para obtener las matrices
        matriz = traslacion @ matriz @ traslacion_inv
        matriz_inv = traslacion_inv @ matriz_inv @ traslacion

        return matriz, matriz_inv

    def _rotacion(self, rotation_angle, rotation_direction):
        
        # 1. Mover los puntos al origen
        traslacion, traslacion_inv = self._traslacion(
            self.x_center, self.y_center
        )
        
        angle_rad = np.radians(rotation_angle)
        if rotation_direction:  # clockwise
            matriz = np.array(
                [
                    [np.cos(angle_rad), np.sin(angle_rad), 0],
                    [-np.sin(angle_rad), np.cos(angle_rad), 0],
                    [0, 0, 1],
                ]
            )
            matriz_inv = np.array(
                [
                    [np.cos(angle_rad), -np.sin(angle_rad), 0],
                    [np.sin(angle_rad), np.cos(angle_rad), 0],
                    [0, 0, 1],
                ]
            )
        else:  # counterclockwise
            matriz = np.array(
                [
                    [np.cos(angle_rad), -np.sin(angle_rad), 0],
                    [np.sin(angle_rad), np.cos(angle_rad), 0],
                    [0, 0, 1],
                ]
            )
            matriz_inv = np.array(
                [
                    [np.cos(angle_rad), np.sin(angle_rad), 0],
                    [-np.sin(angle_rad), np.cos(angle_rad), 0],
                    [0, 0, 1],
                ]
            )
        # ahora hacemos la combinación de las matrices
        matriz = traslacion @ matriz @ traslacion_inv
        matriz_inv = traslacion_inv @ matriz_inv @ traslacion
        
        return matriz, matriz_inv

    def _shearing(self, shearing_x, shearing_y):
        
        # 1. Mover los puntos al origen
        traslacion, traslacion_inv = self._traslacion(
            self.x_center, self.y_center
        )
        
        # Cizallamiento en X
        matriz_x = np.array([[1, shearing_x, 0], [0, 1, 0], [0, 0, 1]])

        # Cizallamiento en Y
        matriz_y = np.array([[1, 0, 0], [shearing_y, 1, 0], [0, 0, 1]])

        # Combinación de las matrices de cizallamiento
        matriz = matriz_y @ matriz_x  # Primero aplicar shearing en X y luego en Y

        # Inversa de las matrices
        matriz_inv_x = np.array([[1, -shearing_x, 0], [0, 1, 0], [0, 0, 1]])

        matriz_inv_y = np.array([[1, 0, 0], [-shearing_y, 1, 0], [0, 0, 1]])

        # Combinación de las matrices inversas
        matriz_inv = (
            matriz_inv_x @ matriz_inv_y
        )  # Primero revertir shearing en Y y luego en X
        
        # ahora hacemos la combinación de las matrices
        matriz = traslacion @ matriz @ traslacion_inv
        matriz_inv = traslacion_inv @ matriz_inv @ traslacion

        return matriz, matriz_inv

    def _reflexion(self, reflexion_modo, pendiente, ordenada):
        if reflexion_modo == Texts.REFLEXION_Y_AXIS:
            matriz = np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]])

        elif reflexion_modo == Texts.REFLEXION_X_AXIS:
            matriz = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])

        elif reflexion_modo == Texts.REFLEXION_ORIGEN:
            matriz = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])

        elif reflexion_modo == Texts.REFLEXION_LINE:
            m = pendiente if pendiente is not None else 0
            b = ordenada if ordenada is not None else 0

            # 1. Mover los puntos acorde a b (traslación)
            matriz_traducir_a_origen = np.array([[1, 0, 0], [0, 1, -b], [0, 0, 1]])

            # 2. Rotación sobre el eje X para que la línea quede horizontal
            angulo_rotacion = np.arctan(m)
            matriz_rotacion = np.array(
                [
                    [np.cos(-angulo_rotacion), -np.sin(-angulo_rotacion), 0],
                    [np.sin(-angulo_rotacion), np.cos(-angulo_rotacion), 0],
                    [0, 0, 1],
                ]
            )

            # 3. Reflexión sobre el eje X
            matriz_reflexion = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])

            # 4. Rotación inversa para volver a la posición original
            matriz_rotacion_inversa = np.array(
                [
                    [np.cos(angulo_rotacion), -np.sin(angulo_rotacion), 0],
                    [np.sin(angulo_rotacion), np.cos(angulo_rotacion), 0],
                    [0, 0, 1],
                ]
            )

            # 5. Mover b a la inversa (traslación)
            matriz_traducir_a_posicion_final = np.array(
                [[1, 0, 0], [0, 1, b], [0, 0, 1]]
            )

            # Combinación de todas las matrices
            matriz = (
                matriz_traducir_a_posicion_final
                @ matriz_rotacion_inversa
                @ matriz_reflexion
                @ matriz_rotacion
                @ matriz_traducir_a_origen
            )

            # Inversa: debemos aplicar el orden inverso
            matriz_inv = (
                matriz_traducir_a_origen
                @ matriz_rotacion
                @ matriz_reflexion
                @ matriz_rotacion_inversa
                @ matriz_traducir_a_posicion_final
            )
        else:
            matriz = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # no rotamos
        # La inversa de una reflexión es la misma operación (reflejar de vuelta te lleva al mismo sitio)
        return matriz, matriz

    def transformar(self, puntos):
        """
        Aplica la matriz de transformación a los puntos dados.

        Argumentos:
            puntos (np.ndarray): Matriz de puntos a transformar.

        Retorna:
            np.ndarray: Los puntos transformados.
        """
        return (self.matriz_transformacion @ puntos).astype(int)
    
    def revertir(self, puntos):
        """
        Aplica la matriz de transformación a los puntos dados.

        Argumentos:
            puntos (np.ndarray): Matriz de puntos a transformar.

        Retorna:
            np.ndarray: Los puntos transformados.
        """
        return (self.matriz_inversa @ puntos).astype(int)
