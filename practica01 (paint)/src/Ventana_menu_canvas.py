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

# Módulos locales
from ventana_menu import VentanaMenu
from punto import Punto
from forma import AlgoritmoDibujo, Linea, Figura
from constantes import Default, UserEvents, Color, Texts


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
        self._punto_inicial: Punto | None = None  # Punto donde comienza el trazo
        self._punto_final: Punto | None = None  # Punto donde finaliza el trazo
        self._figuras: Figura = Figura()  # Colección de figuras dibujadas en el lienzo
        self._nivel_zoom: float = Default.ZOOM_FACTOR  # Nivel actual de zoom
        self._lineas_seleccionadas: list[Linea] = []  # Lista de líneas seleccionadas
        self._offset_x: int = 0  # Desplazamiento horizontal para mover líneas
        self._offset_y: int = 0  # Desplazamiento vertical para mover líneas
        self._scroll_total = 2000  # Máximo desplazamiento de scroll permitido
        self._grupos_figuras: list[Figura] = []  # Lista que almacena grupos de figuras

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
        lienzo.bind(UserEvents.LEFT_DRAG, self._dibujar_en_movimiento)
        lienzo.bind(UserEvents.LEFT_RELEASE, self._terminar_dibujo)
        lienzo.bind(UserEvents.RIGHT_CLICK, self._seleccionar_linea)
        lienzo.bind(UserEvents.MOUSE_WHEEL, self._zoom)

        # Vincular teclas WASD para mover líneas seleccionadas
        self.ventana.bind(
            UserEvents.TECLA_UP, lambda e: self._mover_linea(0, self.tamanho_pincel)
        )  # Arriba
        self.ventana.bind(
            UserEvents.TECLA_LEFT, lambda e: self._mover_linea(-self.tamanho_pincel, 0)
        )  # Izquierda
        self.ventana.bind(
            UserEvents.TECLA_DOWN, lambda e: self._mover_linea(0, -self.tamanho_pincel)
        )  # Abajo
        self.ventana.bind(
            UserEvents.TECLA_RIGHT, lambda e: self._mover_linea(self.tamanho_pincel, 0)
        )  # Derecha

        # Asignar eventos para comandos adicionales
        self.ventana.bind(UserEvents.SPACE, self._realizar_accion)
        self.ventana.bind(
            UserEvents.CONTROL_Z, lambda e: self._deshacer_accion()
        )  # Control + Z para deshacer

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

        self.lienzo.xview_scroll(121, tk.UNITS)
        self.lienzo.yview_scroll(172, tk.UNITS)

    def _crear_punto(self, x: int, y: int) -> Punto:
        x_canvas = self.lienzo.canvasx(x)  # Obtener la coordenada X relativa al canvas
        y_canvas = self.lienzo.canvasy(y)  # Obtener la coordenada Y relativa al canvas
        return Punto(x_canvas, y_canvas)

    def _iniciar_dibujo(self, evento: tk.Event) -> None:
        """
        Inicia el proceso de dibujo cuando el usuario hace clic izquierdo en el lienzo.

        Args:
            evento (tk.Event): Evento de clic del ratón que contiene las coordenadas.
        """
        self._punto_inicial = self._crear_punto(evento.x, evento.y)

    def _dibujar_en_movimiento(self, evento: tk.Event) -> None:
        """
        Dibuja una línea temporal en el lienzo mientras el ratón se mueve,
        mostrando una vista previa de la línea.

        Args:
            evento (tk.Event): Evento de movimiento del ratón.
        """
        if self._punto_inicial:
            punto_provisional = self._crear_punto(evento.x, evento.y)
            self._actualizar_linea_temporal(punto_provisional.x, punto_provisional.y)

    def _actualizar_linea_temporal(self, x: int, y: int) -> None:
        """
        Actualiza la línea temporal en el lienzo, utilizada como una vista previa
        mientras el usuario está dibujando.

        Args:
            x (int): Coordenada X del punto actual.
            y (int): Coordenada Y del punto actual.
        """
        self._lienzo.delete("linea_temporal")  # Elimina la línea temporal previa
        self._lienzo.create_line(
            self._punto_inicial.x,
            self._punto_inicial.y,
            x,
            y,
            fill=self.color_seleccionado,
            tags="linea_temporal",  # Etiqueta usada para identificar la línea temporal
        )

    def _terminar_dibujo(self, evento: tk.Event) -> None:
        """
        Completa el proceso de dibujo y almacena la nueva línea en la colección
        de figuras.

        Args:
            evento (tk.Event): Evento de liberación del botón del ratón.
        """
        if not self._punto_inicial:
            return  # No hay nada que dibujar si el punto inicial no está definido

        self._punto_final = self._crear_punto(evento.x, evento.y)
        self._lienzo.delete("linea_temporal")  # Elimina la línea temporal

        # Crea y almacena una nueva línea
        # Con las coordenadas ajustadas
        self._punto_inicial = self.ajustar_coordenadas(self._punto_inicial, self.tamanho_pincel)
        self._punto_final = self.ajustar_coordenadas(self._punto_final, self.tamanho_pincel)
        
        nueva_linea = Linea(
            self._punto_inicial,
            self._punto_final,
            self._lienzo,
            self.color_seleccionado,
            self.herramienta_seleccionada,
            self.tamanho_pincel,
        )
        self._figuras.anhadir(nueva_linea)
        print(nueva_linea)
        lista_puntos = nueva_linea.dibujar()

        # Ejecuta el comando de dibujo y lo añade al historial
        # comando_dibujo = _DibujarLineaCommand(self._lienzo, nueva_linea, lista_puntos)
        # lista_puntos = self._command_manager.execute(comando_dibujo)
        # print(lista_puntos)
        self._anadir_texto(lista_puntos)

        # Reinicia los puntos
        self._punto_inicial, self._punto_final = None, None
        
    def ajustar_coordenadas(self, punto: Punto, tamanho_pincel: int) -> Punto:
        """
        Encuentra el punto medio del píxel en el que está el punto dado, basado en el tamaño del pincel.
        Ademas, cambia la y de signo para que esten las positivas hacia arriba

        Args:
            punto (Punto): Coordenadas del punto (x, y).
            tamanho_pincel (int): Tamaño del pincel que define el tamaño del píxel.

        Returns:
            Punto: Punto con las coordenadas ajustadas.
        """

        # Encontrar las coordenadas del punto medio del píxel
        x_medio = (punto.x // tamanho_pincel) * tamanho_pincel + tamanho_pincel // 2
        y_medio = (-punto.y // tamanho_pincel) * tamanho_pincel + tamanho_pincel // 2

        return Punto(x_medio, y_medio)
    def _seleccionar_linea(self, event: tk.Event) -> None:
        """
        Selecciona una línea o figura, o múltiples líneas si se mantiene presionada una tecla modificadora.
        """
        punto_real = self._crear_punto(event.x, event.y)

        # Comportamiento normal si no se mantiene Shift presionado
        if not event.state & 0x0001:  # Verifica si Shift no está presionado
            # Restablecer el color de todas las líneas seleccionadas
            for figura in self._lineas_seleccionadas:
                figura.cambiar_outline(figura.color)
            self._lineas_seleccionadas.clear()

        # Buscar la nueva figura cercana al punto clicado
        for figura in self._figuras:
            if (
                isinstance(figura, Linea)
                and self._es_cercano_a_linea(punto_real.x, punto_real.y, figura)
            ) or (
                isinstance(figura, Figura)
                and self._es_cercano_a_figura(punto_real.x, punto_real.y, figura)
            ):
                if figura not in self._lineas_seleccionadas:
                    self._lineas_seleccionadas.append(figura)
                    figura.cambiar_outline("red")  # Marcarla como seleccionada
                else:
                    # Si la figura ya estaba seleccionada, deseleccionarla
                    self._lineas_seleccionadas.remove(figura)
                    figura.cambiar_outline(figura.color)
                break  # Deja de buscar después de encontrar la primera figura

    def _es_cercano_a_figura(self, x: int, y: int, figura: Figura) -> bool:
        """
        Verifica si un punto está cerca de una figura compuesta por líneas.
        """
        for linea in figura._elementos:
            if self._es_cercano_a_linea(x, y, linea):
                return True
        return False

    def _es_cercano_a_linea(self, x: int, y: int, linea: Linea) -> bool:
        """
        Verifica si el punto (x, y) está lo suficientemente cerca de la línea
        especificada.

        Args:
            x (int): Coordenada X del punto.
            y (int): Coordenada Y del punto.
            linea (Linea): Línea con la que se compara la distancia.

        Returns:
            bool: True si el punto está cerca de la línea, False en caso contrario.
        """
        x1, y1 = linea.punto_inicial.x, -linea.punto_inicial.y
        x2, y2 = linea.punto_final.x, -linea.punto_final.y
        distancia_minima = Default.MIN_DISTANCE

        # Cálculo de la distancia entre el punto (x, y) y la línea definida por (x1, y1) y (x2, y2)
        distancia_punto_a_linea = abs(
            (y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1
        ) / (((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5)

        # Cálculo de la distancia acumulada desde el punto (x, y) hasta los puntos finales de la línea
        distancia_acumulada = abs(y - y1) + abs(y - y2) + abs(x - x1) + abs(x - x2)

        # Verifica si cualquiera de las distancias es menor que la distancia mínima permitida
        return min(distancia_punto_a_linea, distancia_acumulada) < distancia_minima

    def _mover_linea(self, x, y) -> None:
        """
        Mueve la línea seleccionada en el lienzo de acuerdo al desplazamiento
        del cursor del ratón.

        Args:
            event (tk.Event): Evento de movimiento del ratón.
        """
        for figura in self._lineas_seleccionadas:
            grupo = self.pertenece_grupo(figura)
            if grupo is not None:
                grupo.mover(x, y)
            else:
                figura.mover(x, y)

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
        self.lienzo.xview_scroll(-19, tk.UNITS)
        self.lienzo.yview_scroll(-24, tk.UNITS)

    def _borrar_todo(self) -> None:
        """
        Borra todo el contenido del lienzo y resetea el estado de las figuras dibujadas.
        """
        super()._borrar_todo()
        self._lienzo.delete("all")
        self._figuras.eliminar_todo()
        self._crear_ejes()

    def _deshacer_accion(self):

        if len(self._figuras.elementos) != 0:
            super()._deshacer_accion()
            ultimo = self._figuras._elementos.pop()
            self._figuras.eliminar(ultimo)

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

    def _realizar_accion(self, event: tk.Event):

        if self._accion == Texts.SECTION_ACTIONS_DELETE:
            self._borrar()

        elif self._accion == Texts.SECTION_ACTIONS_CHANGE_COLOR:
            self._cambiar_color()

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

    def _cambiar_color(self):
        color = self._abrir_seleccion_color()
        for linea in self._lineas_seleccionadas:
            linea.cambiar_color(color)

            grupo = self.pertenece_grupo(linea)
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
        for (
            grupo
        ) in self._grupos_figuras:  # Asumiendo que self.grupos es una lista de grupos
            if (
                linea in grupo._elementos
            ):  # Asumiendo que cada grupo tiene una lista de líneas
                return grupo
        return None

    def _borrar(self) -> None:
        """
        Borra las líneas seleccionadas del lienzo y de la lista de figuras.
        """
        # Crear una copia de la lista de líneas seleccionadas
        lineas_a_borrar = self._lineas_seleccionadas.copy()

        for linea in lineas_a_borrar:
            linea.borrar()  # Llama al método para borrar la línea del lienzo
            self._lineas_seleccionadas.remove(
                linea
            )  # Elimina de la lista de líneas seleccionadas
            self.figuras.eliminar(linea)  # Elimina de la lista de figuras
            grupo = self.pertenece_grupo(linea)
            if grupo is not None:
                grupo.borrar()

    def _agrupar_figuras(self) -> None:
        """
        Agrupa las líneas seleccionadas en un nuevo grupo (Figura).
        """
        if self._lineas_seleccionadas:
            nuevo_grupo = Figura()

            for linea in self._lineas_seleccionadas:
                nuevo_grupo.anhadir(linea)

            self._grupos_figuras.append(nuevo_grupo)
            print(f"Nuevo grupo creado con {len(self._lineas_seleccionadas)} líneas.")

            # Desmarcar las líneas seleccionadas
            for linea in self._lineas_seleccionadas:
                linea.cambiar_outline(linea.color)
            self._lineas_seleccionadas.clear()

    def _desagrupar_figuras(self) -> None:
        """
        Desagrupa las líneas seleccionadas si pertenecen a un grupo.
        """
        if self._lineas_seleccionadas:
            for figura in self._grupos_figuras:
                if any(
                    linea in figura._elementos for linea in self._lineas_seleccionadas
                ):
                    # Eliminar el grupo
                    self._grupos_figuras.remove(figura)
                    print(f"Grupo desagregado: {figura}")

                    # Mover las líneas del grupo fuera
                    for linea in figura._elementos:
                        if isinstance(linea, Linea):
                            self._figuras.anhadir(linea)

                    # Desmarcar las líneas seleccionadas
                    for linea in self._lineas_seleccionadas:
                        linea.cambiar_outline(linea.color)
                    self._lineas_seleccionadas.clear()
                    return

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
