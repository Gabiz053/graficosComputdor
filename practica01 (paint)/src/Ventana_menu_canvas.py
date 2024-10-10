"""
Archivo: Ventana_menu_canvas.py

Este archivo contiene la definición de la clase `VentanaMenuCanvas`, que extiende
la funcionalidad de la clase `VentanaMenu` añadiendo un lienzo (canvas) interactivo
con capacidades de dibujo. Permite a los usuarios dibujar, seleccionar y manipular
figuras en el lienzo, así como aplicar comandos de deshacer y rehacer.

Autor: Gabriel Gomez Garcia
Fecha: 21 de septiembre de 2024
"""

# Librerías estándar
import tkinter as tk

# Módulos locales
from ventana_menu import VentanaMenu
from punto import Punto
from forma import AlgoritmoDibujo, Linea, Figura
from constantes import Default, UserEvents


class _CommandManager:
    """
    Clase interna para gestionar el historial de comandos de dibujo,
    permitiendo operaciones de deshacer (undo) y rehacer (redo).

    Atributos:
        _history (list): Lista que almacena los comandos ejecutados.
        _redo_stack (list): Pila que almacena los comandos deshechos para rehacer.
    """

    def __init__(self) -> None:
        """
        Inicializa un nuevo `CommandManager` con una lista vacía para el historial
        de comandos ejecutados y una pila para los comandos deshechos.
        """
        self._history: list = []  # Historial de comandos ejecutados
        self._redo_stack: list = []  # Pila de comandos deshechos para rehacer

    def execute(self, command: object) -> None:
        """
        Ejecuta un comando, lo almacena en el historial y borra la pila de comandos deshechos.

        Args:
            command (object): El comando que se va a ejecutar. Debe implementar los métodos `execute` y `undo`.
        """
        command.execute()
        self._history.append(command)
        self._redo_stack.clear()  # Se borra la pila de redo al ejecutar un nuevo comando

    def undo(self) -> None:
        """
        Deshace el último comando ejecutado y lo mueve a la pila de comandos deshechos.
        Si no hay comandos en el historial, no hace nada.
        """
        if self._history:
            command = self._history.pop()  # Recupera el último comando ejecutado
            command.undo()  # Deshace el comando
            self._redo_stack.append(
                command
            )  # Añade el comando deshecho a la pila de redo

    def redo(self) -> None:
        """
        Rehace el último comando deshecho, ejecutándolo de nuevo y añadiéndolo
        de vuelta al historial de comandos ejecutados.
        Si no hay comandos para rehacer, no hace nada.
        """
        if self._redo_stack:
            command = self._redo_stack.pop()  # Recupera el último comando deshecho
            command.execute()  # Rehace el comando
            self._history.append(
                command
            )  # Lo añade nuevamente al historial de comandos ejecutados


class _DibujarLineaCommand:
    """
    Comando que encapsula la acción de dibujar una línea en el lienzo, implementando
    la lógica de deshacer y rehacer para gestionar el dibujo de la línea.

    Atributos:
        _lienzo (tk.Canvas): El lienzo (Canvas de Tkinter) donde se dibuja la línea.
        _linea (Linea): La instancia de la clase `Linea` que contiene los puntos y la información de la línea.
    """

    def __init__(self, lienzo: tk.Canvas, linea: "Linea") -> None:
        """
        Inicializa el comando de dibujo con el lienzo donde se va a dibujar la línea
        y la instancia de la línea.

        Args:
            lienzo (tk.Canvas): El lienzo (Canvas) de Tkinter donde se va a dibujar la línea.
            linea (Linea): Instancia de la clase `Linea` que contiene los puntos inicial y final,
                           el color, el tamaño del pincel y otros parámetros.
        """
        self._lienzo: tk.Canvas = lienzo  # Lienzo donde se dibuja la línea
        self._linea: Linea = (
            linea  # Objeto `Linea` que contiene la información del dibujo
        )

    def execute(self) -> None:
        """
        Ejecuta la acción de dibujar la línea en el lienzo.
        Llama al método `dibujar` de la clase `Linea`.
        """
        self._linea.dibujar()

    def undo(self) -> None:
        """
        Deshace la acción de dibujar la línea, eliminándola del lienzo.
        Llama al método `borrar` de la clase `Linea`.
        """
        self._linea.borrar()


class VentanaMenuCanvas(VentanaMenu):
    """
    Clase que extiende 'VentanaMenu', añadiendo la funcionalidad de un lienzo
    (canvas) interactivo donde el usuario puede dibujar formas, realizar zoom,
    y manipular figuras. Permite el uso de diferentes herramientas de dibujo.
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
        Constructor de la clase VentanaMenuCanvas. Inicializa la ventana con
        un lienzo interactivo, configurando tamaño, título y otras propiedades.

        Args:
            width (int): Ancho de la ventana.
            height (int): Alto de la ventana.
            title (str): Título de la ventana.
            color_seleccionado (str): Color por defecto para dibujar.
            herramienta_seleccionada (AlgoritmoDibujo): Herramienta de dibujo seleccionada por defecto.
            tamanho_pincel (int): Tamaño del pincel usado para dibujar.
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
        self._linea_seleccionada: Linea | None = None  # Línea seleccionada
        self._offset_x: int = 0  # Offset horizontal para el movimiento de líneas
        self._offset_y: int = 0  # Offset vertical para el movimiento de líneas
        self._command_manager = _CommandManager()  # Gestor de deshacer/rehacer

    def _crear_contenido_ventana(self) -> None:
        """
        Sobrescribe el método de `VentanaMenu` para añadir el lienzo de dibujo
        a la ventana.
        """
        super()._crear_contenido_ventana()
        self._crear_lienzo()

    def _crear_lienzo(self) -> None:
        """
        Modifica el lienzo para asignar eventos del ratón para la
        interacción y devuelve la referencia al lienzo.
        """
        lienzo = self.lienzo
        lienzo.config(scrollregion=lienzo.bbox("all"))

        # Asignar eventos del ratón para interactuar con el lienzo
        lienzo.bind(UserEvents.LEFT_CLICK, self._iniciar_dibujo)
        lienzo.bind(UserEvents.LEFT_DRAG, self._dibujar_en_movimiento)
        lienzo.bind(UserEvents.LEFT_RELEASE, self._terminar_dibujo)
        lienzo.bind(UserEvents.RIGHT_CLICK, self._seleccionar_linea)
        lienzo.bind(UserEvents.RIGHT_DRAG, self._mover_linea)
        lienzo.bind(UserEvents.RIGHT_RELEASE, self._finalizar_mover_linea)
        lienzo.bind(UserEvents.MOUSE_WHEEL, self._zoom)

    ########### Manejo de eventos ###########

    def _iniciar_dibujo(self, evento: tk.Event) -> None:
        """
        Inicia el proceso de dibujo cuando el usuario hace clic izquierdo en el lienzo.

        Args:
            evento (tk.Event): Evento de clic del ratón que contiene las coordenadas.
        """
        self._punto_inicial = Punto(evento.x, evento.y)

    def _dibujar_en_movimiento(self, evento: tk.Event) -> None:
        """
        Dibuja una línea temporal en el lienzo mientras el ratón se mueve,
        mostrando una vista previa de la línea.

        Args:
            evento (tk.Event): Evento de movimiento del ratón.
        """
        if self._punto_inicial:
            self._actualizar_linea_temporal(evento.x, evento.y)

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

        self._punto_final = Punto(evento.x, evento.y)
        self._lienzo.delete("linea_temporal")  # Elimina la línea temporal

        # Crea y almacena una nueva línea
        nueva_linea = Linea(
            self._punto_inicial,
            self._punto_final,
            self._lienzo,
            self.color_seleccionado,
            self.herramienta_seleccionada,
            self.tamanho_pincel,
        )
        self._figuras.anhadir(nueva_linea)

        # Ejecuta el comando de dibujo y lo añade al historial
        comando_dibujo = _DibujarLineaCommand(self._lienzo, nueva_linea)
        self._command_manager.execute(comando_dibujo)

        # Reinicia los puntos
        self._punto_inicial, self._punto_final = None, None

    def _seleccionar_linea(self, event: tk.Event) -> None:
        """
        Selecciona una línea del lienzo si el cursor está lo suficientemente
        cerca de ella, permitiendo su manipulación posterior.

        Args:
            event (tk.Event): Evento de clic del ratón.
        """
        self._linea_seleccionada = None
        for linea in self._figuras:
            if isinstance(linea, Linea) and self._es_cercano_a_linea(
                event.x, event.y, linea
            ):
                self._linea_seleccionada = linea
                break

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
        x1, y1 = linea.punto_inicial.x, linea.punto_inicial.y
        x2, y2 = linea.punto_final.x, linea.punto_final.y
        distancia_minima = Default.MIN_DISTANCE

        # Cálculo de la distancia entre el punto (x, y) y la línea definida por (x1, y1) y (x2, y2)
        distancia_punto_a_linea = abs(
            (y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1
        ) / (((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5)

        # Cálculo de la distancia acumulada desde el punto (x, y) hasta los puntos finales de la línea
        distancia_acumulada = abs(y - y1) + abs(y - y2) + abs(x - x1) + abs(x - x2)

        # Verifica si cualquiera de las distancias es menor que la distancia mínima permitida
        return min(distancia_punto_a_linea, distancia_acumulada) < distancia_minima

    def _mover_linea(self, event: tk.Event) -> None:
        """
        Mueve la línea seleccionada en el lienzo de acuerdo al desplazamiento
        del cursor del ratón.

        Args:
            event (tk.Event): Evento de movimiento del ratón.
        """
        if self._linea_seleccionada:
            new_x1 = event.x - self._offset_x
            new_y1 = event.y - self._offset_y
            self._linea_seleccionada.mover(new_x1, new_y1)

    def _finalizar_mover_linea(self, event: tk.Event) -> None:
        """
        Finaliza el proceso de movimiento de la línea seleccionada.

        Args:
            event (tk.Event): Evento de liberación del ratón.
        """
        self._linea_seleccionada = None

    def _zoom(self, evento: tk.Event) -> None:
        """
        Ajusta el nivel de zoom del lienzo según el desplazamiento de la rueda del ratón.

        Args:
            evento (tk.Event): Evento de desplazamiento del ratón.
        """
        scale_factor = (
            Default.ZOOM_IN_FACTOR if evento.delta > 0 else Default.ZOOM_OUT_FACTOR
        )
        nuevo_nivel_zoom = self._nivel_zoom * scale_factor

        # Limita el nivel de zoom a un rango entre 0.5x y 3x
        if Default.ZOOM_LIMIT_MIN <= nuevo_nivel_zoom <= Default.ZOOM_LIMIT_MAX:
            self._nivel_zoom = nuevo_nivel_zoom
            # falta escalar los puntos de las lineas desde dentro de la linea
            self._lienzo.scale("all", evento.x, evento.y, scale_factor, scale_factor)

    def _borrar_todo(self) -> None:
        """
        Borra todo el contenido del lienzo y resetea el estado de las figuras dibujadas.
        """
        super()._borrar_todo()
        self._lienzo.delete("all")
        self._figuras.eliminar_todo()

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
    def linea_seleccionada(self) -> Linea | None:
        """Devuelve la línea actualmente seleccionada."""
        return self._linea_seleccionada

    @linea_seleccionada.setter
    def linea_seleccionada(self, valor: Linea) -> None:
        """Establece la línea seleccionada para manipulación."""
        self._linea_seleccionada = valor

    @property
    def nivel_zoom(self) -> float:
        """Devuelve el nivel actual de zoom del lienzo."""
        return self._nivel_zoom

    @nivel_zoom.setter
    def nivel_zoom(self, valor: float) -> None:
        """Establece el nivel de zoom del lienzo."""
        self._nivel_zoom = valor
