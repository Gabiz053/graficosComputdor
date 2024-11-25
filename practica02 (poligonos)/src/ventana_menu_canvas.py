"""
Archivo: ventana_menu_canvas.py

Descripción:
    Este archivo define la clase `VentanaMenuCanvas`, que amplía las funcionalidades 
    de la clase `VentanaMenu` al incorporar un lienzo interactivo para dibujo. 
    Los usuarios pueden dibujar, seleccionar y manipular figuras en el lienzo, 
    además de contar con opciones para deshacer y rehacer acciones.

Autor: Gabriel Gomez Garcia
Fecha: 21 de septiembre de 2024
"""

# Librerías estándar
import tkinter as tk
import numpy as np

# Módulos locales
from ventana_menu import VentanaMenu
from punto import Punto
from forma import Poligono, Figura
from algoritmos_dibujo import AlgoritmoDibujo
from constantes import Default, UserEvents, Color, Texts
from transformaciones import Transformacion

class VentanaMenuCanvas(VentanaMenu):
    """
    Clase `VentanaMenuCanvas`:
    Extiende la clase 'VentanaMenu', añadiendo un lienzo interactivo donde los
    usuarios pueden dibujar formas, realizar zoom y manipular figuras, usando
    diversas herramientas de dibujo.
    """

    def __init__(
        self,
        width: int = Default.WINDOW_WIDTH,
        height: int = Default.WINDOW_HEIGHT,
        title: str = Default.WINDOW_TITLE,
        color_seleccionado: str = Default.DRAWING_COLOR,
        herramienta_seleccionada: AlgoritmoDibujo = Default.DRAWING_TOOL,
        tamanho_pincel: int = Default.DRAWING_SIZE,
    ) -> None:
        """
        Constructor de la clase VentanaMenuCanvas.

        Inicializa una ventana con un lienzo interactivo, configurando el tamaño,
        el título y otras propiedades de dibujo.

        Args:
            width (int): Ancho de la ventana.
            height (int): Alto de la ventana.
            title (str): Título de la ventana.
            color_seleccionado (str): Color por defecto para dibujar.
            herramienta_seleccionada (AlgoritmoDibujo): Herramienta de dibujo seleccionada por defecto.
            tamanho_pincel (int): Tamaño del pincel utilizado para dibujar.
        """
        super().__init__(
            width,
            height,
            title,
            color_seleccionado,
            herramienta_seleccionada,
            tamanho_pincel,
        )

        # Inicialización de variables privadas relacionadas con el dibujo
        self._figuras: Figura = Figura()  # Colección de figuras dibujadas en el lienzo
        self._nivel_zoom: float = Default.ZOOM_FACTOR  # Nivel actual de zoom
        self._poligonos_seleccionados: list[Poligono] = (
            []
        )  # Lista de poligonos seleccionados
        self._scroll_total = 2000  # Máximo desplazamiento de scroll permitido
        self._grupos_figuras: list[Figura] = []  # Lista que almacena grupos de figuras
        self._puntos_poligono = np.empty(
            (3, 0)
        )  # Un array de 3 filas vacio para guardar los puntos
        
        self.lista_transformaciones: list[(Poligono, np.ndarray)] = []  # Lista de transformaciones aplicadas a los poligonos
        self.lista_transformaciones_rehacer: list[(Poligono, np.ndarray)] = []  # Lista de transformaciones que se pueden rehacer

    def _crear_contenido_ventana(self) -> None:
        """
        Sobrescribe el método `VentanaMenu` para añadir el lienzo interactivo
        en la ventana.
        """
        super()._crear_contenido_ventana()
        self._crear_lienzo()

    def _crear_lienzo(self) -> None:
        """
        Configura el lienzo con eventos del ratón para la interacción.
        """
        lienzo = self.lienzo

        self._centrar_canvas()
        self._crear_ejes()

        # Asignar eventos del ratón para interactuar con el lienzo
        lienzo.bind(UserEvents.LEFT_CLICK, self._iniciar_dibujo)
        lienzo.bind(UserEvents.DRAG, self._dibujar_en_movimiento)
        self.ventana.bind(UserEvents.CONTROL_LEFT, self._terminar_dibujo)
        # lienzo.bind(UserEvents.MOUSE_WHEEL, self._zoom)

        lienzo.bind(UserEvents.RIGHT_CLICK, self._seleccionar_poligono)

        # # Asignar eventos para comandos adicionales
        self.ventana.bind(UserEvents.ALT_LEFT, self._realizar_accion)

        # Eventos para mover el lienzo usando las flechas del teclado
        self.ventana.bind(
            UserEvents.ARROW_UP, lambda e: self._mover_canvas(0, -Default.CANVAS_MOVE_Y)
        )  # Mover arriba
        self.ventana.bind(
            UserEvents.ARROW_DOWN,
            lambda e: self._mover_canvas(0, Default.CANVAS_MOVE_Y),
        )  # Mover abajo
        self.ventana.bind(
            UserEvents.ARROW_LEFT,
            lambda e: self._mover_canvas(-Default.CANVAS_MOVE_X, 0),
        )  # Mover izquierda
        self.ventana.bind(
            UserEvents.ARROW_RIGHT,
            lambda e: self._mover_canvas(Default.CANVAS_MOVE_X, 0),
        )  # Mover derecha

        # Asignar eventos para agrupar y desagrupar figuras
        self.ventana.bind(
            UserEvents.TECLA_G, lambda e: self._agrupar_figuras()
        )  # Agrupar con tecla 'G'
        self.ventana.bind(
            UserEvents.TECLA_H, lambda e: self._desagrupar_figuras()
        )  # Desagrupar con tecla 'H'
        
        # cosas de transformaciones
        self.ventana.bind(
            UserEvents.ENTER, lambda e: self._aplicar_transformaciones()
        )  # transformar con tecla 'T'
        self.ventana.bind(
            UserEvents.CONTROL_Z, lambda e: self._deshacer_transformaciones()
        )  # deshacer transformacion hecha
        self.ventana.bind(
            UserEvents.CONTROL_Y, lambda e: self._rehacer_transformaciones()
        )  # rehacer transformacion borrada
        
        # cosas peli
        self.ventana.bind(
            UserEvents.SPACE, lambda e: self._guardar_frame()
        )  # generar un frame de la peli

    ########### Manejo de eventos ###########
    def _crear_ejes(self) -> None:
        self.lienzo.create_line(-2000, 0, 2000, 0, fill=Color.GRAY, width=1)  # Eje X
        self.lienzo.create_line(0, 2000, 0, -2000, fill=Color.GRAY, width=1)  # Eje Y

    def _centrar_canvas(self) -> None:
        # Configurar el área desplazable (scrollregion) más amplia para que el origen esté en el centro
        self.lienzo.configure(
            scrollregion=(
                -self._scroll_total,
                -self._scroll_total,
                self._scroll_total,
                self._scroll_total,
            )
        )
        self.lienzo.xview_scroll(-10000, tk.UNITS)
        self.lienzo.yview_scroll(-10000, tk.UNITS)

        self.lienzo.xview_scroll(37, tk.UNITS)
        self.lienzo.yview_scroll(55, tk.UNITS)

    def _crear_punto(self, x: int, y: int) -> Punto:
        x_canvas = self.lienzo.canvasx(x)  # Obtener la coordenada X relativa al canvas
        y_canvas = self.lienzo.canvasy(y)  # Obtener la coordenada Y relativa al canvas
        return Punto(x_canvas, y_canvas)

    def _iniciar_dibujo(self, evento: tk.Event) -> None:
        """Inicia el proceso de dibujo cuando el usuario hace clic izquierdo en el lienzo."""

        # va a servir tanto para empezar el dibujo como para anhadir mas puntos
        # ya que es al terminar cuando gestionamos que se borre todo lo demas
        # conseguimos toda la info del punto  donde se hizo clic
        punto_actual = self._crear_punto(evento.x, evento.y)

        # posibles casos:

        # con 2 o menos puntos no va a haber poligono, anhadimos el punto sin mas
        if self._puntos_poligono.shape[1] <= 2:
            self._puntos_poligono = np.append(
                self._puntos_poligono, [[punto_actual.x], [punto_actual.y], [1]], axis=1
            )

        # puede haber poligono y sabemos que tenemos 3 puntos al menos
        else:
            # el punto inicial
            punto_inicial = self._puntos_poligono[:, 0]

            # si el punto  actual esta cerca del inicial, no anadimos nada y cerramos
            # Coordenadas del punto inicial
            x1 = punto_inicial[0]  # x del punto inicial
            y1 = punto_inicial[1]  # y del punto inicial

            # Coordenadas del otro punto
            x2 = punto_actual.x
            y2 = punto_actual.y

            # Calcula la distancia
            distancia_puntos = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

            # si estan cerquita , cerramos el poligono
            if distancia_puntos < Default.MIN_DISTANCE_SELECT:
                self._terminar_dibujo(evento)

            # si no pues otro punto
            else:
                self._puntos_poligono = np.append(
                    self._puntos_poligono,
                    [[punto_actual.x], [punto_actual.y], [1]],
                    axis=1,
                )

        # print(self._puntos_poligono)

    def _dibujar_en_movimiento(self, evento: tk.Event) -> None:
        """
        Dibuja una línea temporal en el lienzo mientras el ratón se mueve,
        mostrando una vista previa de la línea.

        Args:
            evento (tk.Event): Evento de movimiento del ratón.
        """
        if self._puntos_poligono.size != 0:
            punto_provisional = self._crear_punto(evento.x, evento.y)
            self._actualizar_linea_temporal(punto_provisional.x, punto_provisional.y)

    def _actualizar_linea_temporal(self, x: int, y: int) -> None:
        """
        Actualiza las líneas temporales en el lienzo, mostrando una vista previa
        de todo el polígono mientras el usuario está dibujando.

        Args:
            x (int): Coordenada X del punto actual.
            y (int): Coordenada Y del punto actual.
        """
        self._lienzo.delete("linea_temporal")  # Elimina las líneas temporales previas

        # Dibuja líneas entre los puntos existentes
        num_puntos = self._puntos_poligono.shape[1]  # Número de puntos en el polígono

        for i in range(num_puntos - 1):
            p1 = self._puntos_poligono[:, i]  # Punto i
            p2 = self._puntos_poligono[:, i + 1]  # Punto i+1
            self._lienzo.create_line(
                p1[0],
                p1[1],
                p2[0],
                p2[1],
                fill=self.color_seleccionado,
                tags="linea_temporal",  # Etiqueta usada para identificar la línea temporal
            )

        # Dibuja la línea desde el último punto hasta el punto actual
        ultimo_punto = self._puntos_poligono[:, -1]
        self._lienzo.create_line(
            ultimo_punto[0],
            ultimo_punto[1],
            x,
            y,
            fill=self.color_seleccionado,
            tags="linea_temporal",
        )

    def _terminar_dibujo(self, evento: tk.Event) -> None:
        """
        Completa el proceso de dibujo y almacena el nuevo polígono en la colección de figuras.
        """
        # lo pirmero quitar todas las lineas temporales qe hayamos hecho
        self._lienzo.delete("linea_temporal")  # Elimina la línea temporal

        if self._puntos_poligono.size == 0:
            print("prueba a poner algunos puntos en el lienzo!!")
            return  # No hay nada que dibujar si el punto inicial no está definido

        # aqui ya tenemos en puntos poligono todos los puntos en orden
        # lo unico hay que ajustar las coordenadas segun el tamanho del pincel
        # se pueden ajustar todas a la vez!
        puntos_ajustados = self.ajustar_coordenadas(
            self._puntos_poligono, self.tamanho_pincel
        )

        # ahora estan todos los puntos bien ajustados para pintarlos bien
        nuevo_poligono = Poligono(
            puntos_ajustados,
            self._lienzo,
            self.color_seleccionado,
            self.herramienta_seleccionada,
            self.tamanho_pincel,
            self.relleno_activado,
        )

        self._figuras.anhadir(nuevo_poligono)
        print(nuevo_poligono)

        nuevo_poligono.dibujar()

        # una vez acabamos, volvemos a limpiar el poligono para crear otro
        self._puntos_poligono = np.empty((3, 0))

    def ajustar_coordenadas(
        self, puntos: np.ndarray, tamanho_pincel: int
    ) -> np.ndarray:
        """
        Ajusta las coordenadas de los puntos en el array según el tamaño del pincel.
        Cambia la y de signo para que estén las positivas hacia arriba.

        Args:
            puntos (np.ndarray): Array de puntos (3 x n) donde cada columna es un punto (x, y, 1).
            tamanho_pincel (int): Tamaño del pincel que define el tamaño del píxel.

        Returns:
            np.ndarray: Array de puntos ajustados (3 x n).
        """

        # Ajustar las coordenadas
        x_medio = (puntos[0] // tamanho_pincel) * tamanho_pincel + (tamanho_pincel // 2)
        y_medio = (-puntos[1] // tamanho_pincel) * tamanho_pincel + (
            tamanho_pincel // 2
        )

        # Crear un nuevo array con las coordenadas ajustadas
        puntos_ajustados = np.array(
            [x_medio, y_medio, np.ones(puntos.shape[1])], dtype=int
        )

        return puntos_ajustados

    def _seleccionar_poligono(self, event: tk.Event) -> None:
        """
        Selecciona un polígono, o múltiples polígonos si se mantiene presionada una tecla modificadora.
        """
        punto_real = self._crear_punto(event.x, event.y)

        # Comportamiento normal si no se mantiene Shift presionado
        if not event.state & 0x0001:  # Verifica si Shift no está presionado
            # Restablecer el color de todas las líneas seleccionadas
            for figura in self._poligonos_seleccionados:
                figura.cambiar_outline(figura.color)
            self._poligonos_seleccionados.clear()

        # Buscar el nuevo polígono cercano al punto clicado
        for figura in self._figuras:
            if (
                isinstance(figura, Figura)
                and self._es_dentro_figura(punto_real.x, -punto_real.y, figura)
            ) or (
                isinstance(figura, Poligono)
                and self._es_punto_dentro_poligono(punto_real.x, -punto_real.y, figura)
            ):
                if figura not in self._poligonos_seleccionados:
                    self._poligonos_seleccionados.append(figura)
                    figura.cambiar_outline("red")  # Marcarla como seleccionada
                else:
                    # Si la figura ya estaba seleccionada, deseleccionarla
                    self._poligonos_seleccionados.remove(figura)
                    figura.cambiar_outline(figura.color)
                break  # Deja de buscar después de encontrar la primera figura

    def _es_dentro_figura(self, x: int, y: int, figura: Figura) -> bool:
        """
        Verifica si un punto está cerca de una figura compuesta por poligonos.
        """
        for poligono in figura._elementos:
            if self._es_punto_dentro_poligono(x, y, poligono):
                return True
        return False

    def _es_punto_dentro_poligono(self, x: int, y: int, poligono: Poligono) -> bool:
        """
        Verifica si un punto (x, y) está dentro de un polígono.
        """
        puntos = poligono.puntos  # Asumiendo que _puntos_poligono es un array 2D
        n = puntos.shape[1]  # Número de vértices
        dentro = False

        for i in range(n):
            x1, y1 = puntos[0, i], puntos[1, i]
            x2, y2 = puntos[0, (i + 1) % n], puntos[1, (i + 1) % n]

            # Verifica si el rayo cruza el borde del polígono
            if (y1 > y) != (y2 > y):  # El rayo cruza la línea
                # Calcular el punto de intersección
                interseccion_x = (x2 - x1) * (y - y1) / (y2 - y1) + x1
                if x < interseccion_x:  # Solo contar si está a la izquierda del rayo
                    dentro = not dentro
        return dentro

    def _zoom(self, evento: tk.Event) -> None:
        """
        Ajusta el nivel de zoom del lienzo según el desplazamiento de la rueda del ratón.

        Args:
            evento (tk.Event): Evento de desplazamiento del ratón.
        """
        # Factor de escala (Zoom in o Zoom out)
        scale_factor = (
            Default.ZOOM_IN_FACTOR if evento.delta > 0 else Default.ZOOM_OUT_FACTOR
        )

        # Nuevo nivel de zoom a aplicar
        nuevo_nivel_zoom = round(self._nivel_zoom + scale_factor, 1)

        # Limita el nivel de zoom a un rango entre min y max
        if Default.ZOOM_LIMIT_MIN <= nuevo_nivel_zoom <= Default.ZOOM_LIMIT_MAX:
            # Calcula el factor relativo respecto al nivel actual
            zoom = nuevo_nivel_zoom / self._nivel_zoom

            # Actualiza el nivel de zoom
            self._nivel_zoom = nuevo_nivel_zoom

            # Punto donde el cursor está, para hacer el zoom relativo
            punto = self._crear_punto(evento.x, evento.y)

            # Aplica la escala relativa al lienzo
            self._lienzo.scale("all", punto.x, punto.y, zoom, zoom)

            # Actualiza el rango de desplazamiento (scroll)
            self._scroll_total = self._scroll_total + (2000 * scale_factor)
            self.lienzo.configure(
                scrollregion=(
                    -self._scroll_total,
                    -self._scroll_total,
                    self._scroll_total,
                    self._scroll_total,
                )
            )

    def _resetear_zoom(self) -> None:
        """
        Restablece el zoom a su valor predeterminado (zoom=1).
        """
        # Calcular el factor inverso del nivel de zoom actual
        if self._nivel_zoom != 1:
            inverso = 1 / self._nivel_zoom
            self._lienzo.scale("all", 0, 0, inverso, inverso)

        # Restablece el valor del zoom y la región de desplazamiento
        self._nivel_zoom = 1
        self._scroll_total = 2000
        self.lienzo.configure(
            scrollregion=(
                -self._scroll_total,
                -self._scroll_total,
                self._scroll_total,
                self._scroll_total,
            )
        )

        # Centra el canvas
        self._centrar_canvas()
        self.lienzo.xview_scroll(-12, tk.UNITS)
        self.lienzo.yview_scroll(-16, tk.UNITS)

    def _borrar_todo(self) -> None:
        """
        Borra todo el contenido del lienzo y resetea el estado de las figuras dibujadas.
        """
        super()._borrar_todo()
        self._lienzo.delete("all")
        self._figuras.eliminar_todo()
        self._crear_ejes()
        self.lista_transformaciones.clear()
        self.lista_transformaciones_rehacer.clear()

    def _mover_canvas(self, dx: int, dy: int) -> None:
        """
        Desplaza el canvas en función de los valores de desplazamiento proporcionados.

        Args:
            dx (int): Desplazamiento horizontal en unidades.
            dy (int): Desplazamiento vertical en unidades.

        Returns:
            None
        """
        if not isinstance(dx, int) or not isinstance(dy, int):
            raise ValueError("Los valores de desplazamiento deben ser enteros.")

        # Desplazamiento horizontal del canvas
        self.lienzo.xview_scroll(dx, tk.UNITS)

        # Desplazamiento vertical del canvas
        self.lienzo.yview_scroll(dy, tk.UNITS)

    def _seleccionar_agrupar(self) -> None:
        """
        Selecciona la acción de agrupar las líneas o figuras seleccionadas.

        Este método se activa cuando el usuario elige agrupar elementos,
        mostrando un mensaje de confirmación en la consola.
        """
        super()._seleccionar_agrupar()
        self._agrupar_figuras()

    def _seleccionar_desagrupar(self) -> None:
        """
        Selecciona la acción de desagrupar las figuras agrupadas previamente.

        Este método se activa cuando el usuario elige desagrupar, mostrando
        un mensaje de confirmación en la consola.
        """
        super()._seleccionar_desagrupar()
        self._desagrupar_figuras()

    def _agrupar_figuras(self) -> None:
        """
        Agrupa las líneas seleccionadas en un nuevo grupo (Figura).
        """
        if self._poligonos_seleccionados:
            nuevo_grupo = Figura()

            for poligono in self._poligonos_seleccionados:
                nuevo_grupo.anhadir(poligono)

            self._grupos_figuras.append(nuevo_grupo)
            print(
                f"Nuevo grupo creado con {len(self._poligonos_seleccionados)} poligonos."
            )

            # Desmarcar las líneas seleccionadas
            for poligono in self._poligonos_seleccionados:
                poligono.cambiar_outline(poligono.color)
            self._poligonos_seleccionados.clear()

    def _desagrupar_figuras(self) -> None:
        """
        Desagrupa las líneas seleccionadas si pertenecen a un grupo.
        """
        if self._poligonos_seleccionados:
            for figura in self._grupos_figuras:
                if any(
                    poligono in figura._elementos
                    for poligono in self._poligonos_seleccionados
                ):
                    # Eliminar el grupo
                    self._grupos_figuras.remove(figura)
                    print(f"Grupo desagregado: {figura}")

                    # Mover las líneas del grupo fuera
                    for poligono in figura._elementos:
                        if isinstance(poligono, Poligono):
                            self._figuras.anhadir(poligono)

                    # Desmarcar las líneas seleccionadas
                    for poligono in self._poligonos_seleccionados:
                        poligono.cambiar_outline(poligono.color)
                    self._poligonos_seleccionados.clear()
                    return

    def _cambiar_color(self):
        color = self._abrir_seleccion_color()
        for poligono in self._poligonos_seleccionados:
            poligono.cambiar_color(color)

            grupo = self.pertenece_grupo(poligono)
            if grupo is not None:
                grupo.cambiar_color(color)

    def pertenece_grupo(self, linea):
        """
        Verifica si una línea pertenece a un grupo específico.

        Args:
            linea: La línea que se va a verificar.

        Returns:
            bool: True si la línea pertenece al grupo, False en caso contrario.
        """
        for grupo in self._grupos_figuras:
            if linea in grupo._elementos:
                return grupo
        return None

    def _borrar(self) -> None:
        """
        Borra los polígonos seleccionados del lienzo y de la lista de figuras.
        Además, actualiza las listas de deshacer y rehacer para eliminar 
        cualquier transformación asociada a los polígonos eliminados.
        """
        # Crear una copia de los polígonos seleccionados para evitar modificaciones durante la iteración
        poligonos_a_borrar = self._poligonos_seleccionados.copy()

        for poligono in poligonos_a_borrar:
            # Llamar al método para borrar el polígono del lienzo
            poligono.borrar()

            # Eliminar el polígono de las listas internas
            self._poligonos_seleccionados.remove(poligono)
            self._figuras.eliminar(poligono)

            # Eliminar transformaciones asociadas al polígono de las listas de deshacer y rehacer
            self._actualizar_listas_deshacer_rehacer(poligono)

            # Si el polígono pertenece a un grupo, borrar el grupo
            grupo = self.pertenece_grupo(poligono)
            if grupo is not None:
                grupo.borrar()

    def _actualizar_listas_deshacer_rehacer(self, poligono):
        """
        Actualiza las listas de deshacer y rehacer para eliminar 
        cualquier transformación asociada con el polígono dado.
        """
        def filtrar_lista(lista):
            return [tupla for tupla in lista if tupla[0] != poligono]

        # Actualizar las listas
        self.lista_transformaciones = filtrar_lista(self.lista_transformaciones)
        self.lista_transformaciones_rehacer = filtrar_lista(self.lista_transformaciones_rehacer)

        # Depuración: imprime el estado de las figuras y polígonos seleccionados
        print("Figuras restantes:", self._figuras.elementos)
        print("Polígonos seleccionados restantes:", self._poligonos_seleccionados)

    def _realizar_accion(self, event: tk.Event):
        if self._accion == Texts.SECTION_ACTIONS_DELETE:
            self._borrar()

        elif self._accion == Texts.SECTION_ACTIONS_CHANGE_COLOR:
            self._cambiar_color()

    def _aplicar_transformaciones(self) -> dict:
        transformaciones = super()._aplicar_transformaciones()

        # aplicamos la transformacion a cada poligono seleccionado
        for poligono in self._poligonos_seleccionados:
            # guardamos los puntos antes de transformar para poder volver a ellos
            self.lista_transformaciones.append((poligono, poligono.puntos))
            poligono.transformar(transformaciones)
            
            # print(self.lista_transformaciones)
            
    def _deshacer_transformaciones(self):
        if len(self.lista_transformaciones) != 0:
            super()._deshacer_transformaciones()
            poligono, puntos = self.lista_transformaciones.pop()
            # guardamos los puntos antes de transformar para poder volver a ellos
            self.lista_transformaciones_rehacer.append((poligono, poligono.puntos))
            # ahora ponemos al poligono en los puntos anteriores
            poligono.borrar()
            poligono.puntos = puntos
            poligono.dibujar()
        else:
            print("No hay transformaciones para deshacer")
    
    def _rehacer_transformaciones(self):
        if len(self.lista_transformaciones_rehacer) != 0:
            super()._rehacer_transformaciones()
            poligono, puntos = self.lista_transformaciones_rehacer.pop()
            # ya no guardamos nada, se pierde
            # ahora ponemos al poligono en los puntos anteriores
            poligono.borrar()
            poligono.puntos = puntos
            poligono.dibujar()
        else:
            print("No hay transformaciones para rehacer")
    ########### Getters y setters ###########

    @property
    def punto_inicial(self) -> Punto | None:
        """Devuelve el punto inicial del dibujo actual."""
        return self._punto_inicial

    @punto_inicial.setter
    def punto_inicial(self, valor: Punto) -> None:
        """Establece el punto inicial del dibujo."""
        self._punto_inicial = valor

    @property
    def punto_final(self) -> Punto | None:
        """Devuelve el punto final del dibujo actual."""
        return self._punto_final

    @punto_final.setter
    def punto_final(self, valor: Punto) -> None:
        """Establece el punto final del dibujo."""
        self._punto_final = valor

    @property
    def figuras(self) -> Figura:
        """Devuelve la colección de figuras dibujadas en el lienzo."""
        return self._figuras

    @property
    def nivel_zoom(self) -> float:
        """Devuelve el nivel actual de zoom del lienzo."""
        return self._nivel_zoom

    @nivel_zoom.setter
    def nivel_zoom(self, valor: float) -> None:
        """Establece el nivel de zoom del lienzo."""
        self._nivel_zoom = valor
