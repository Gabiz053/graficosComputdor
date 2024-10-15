"""
Archivo: ventana_menu.py

Este archivo define la clase VentanaMenu, que extiende la funcionalidad
de la clase abstracta Ventana. Crea una ventana con un menú para la
aplicación gráfica.

Autor: Gabriel Gomez Garcia
Fecha: 21 de septiembre de 2024
"""

# Imports estándar
import tkinter as tk

# Imports de terceros
import customtkinter as ctk
from CTkColorPicker import AskColor

# Imports locales
from ventana import Ventana
from algoritmos_dibujo import AlgoritmoDibujo
from constantes import Default, DrawingStrategies, MenuLabels, Texts, Color


class VentanaMenu(Ventana):
    """
    Clase que representa una ventana con un menú desplegable interactivo.

    Hereda de la clase abstracta Ventana, añadiendo un menú superior y
    una sección de herramientas para interactuar con el lienzo.

    Atributos heredados:
        _width (int): El ancho de la ventana en píxeles.
        _height (int): La altura de la ventana en píxeles.
        _title (str): El título de la ventana.
        _ventana (ctk.CTk): La instancia de la ventana principal de customtkinter.

    Atributos de instancia:
        _color_seleccionado (str): Color seleccionado para dibujar.
        _herramienta_seleccionada (str): Herramienta seleccionada para dibujar.
        _tamanho_pincel (int): Grosor de las figuras dibujadas.
        _lienzo (ctk.CTkCanvas): Lienzo donde se dibujan las figuras.
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
        Inicializa la ventana con las dimensiones y el título proporcionados.

        Args:
            width (int): Ancho de la ventana en píxeles (por defecto, VENTANA_WIDTH).
            height (int): Alto de la ventana en píxeles (por defecto, VENTANA_HEIGHT).
            title (str): Título de la ventana (por defecto, VENTANA_TITLE).
            color_seleccionado (str): Color seleccionado para dibujar (por defecto, COLOR).
            herramienta_seleccionada (AlgoritmoDibujo): Herramienta seleccionada para dibujar
                (por defecto, HERRAMIENTA).
            tamanho_pincel (int): Grosor de las figuras dibujadas (por defecto, TAMANHO_DIBUJAR).
        """
        super().__init__(width, height, title)
        self._color_seleccionado = color_seleccionado
        self._herramienta_seleccionada = herramienta_seleccionada
        self._tamanho_pincel = tamanho_pincel
        self._lienzo = None
        self._accion = Texts.SECTION_ACTIONS_DELETE

    def _crear_contenido_ventana(self) -> None:
        """
        Configura el contenido de la ventana añadiendo un menú de opciones.

        Este método sobrescribe la función abstracta heredada para implementar
        un menú superior y una barra de herramientas para interactividad.
        """
        self._crear_menu_superior()
        self._crear_menu_herramientas()

    ########### Métodos de selección y actualización ###########

    def _abrir_seleccion_color(self) -> str:
        pick_color = AskColor()  # Abre el selector de color
        return pick_color.get()  # Obtiene la cadena de color

    def _seleccionar_color(self) -> None:
        """Abre un selector de color y actualiza el color seleccionado."""
        self.color_seleccionado = self._abrir_seleccion_color()
        print(f"{Texts.SELECT_COLOR} {self.color_seleccionado}")

    def _seleccionar_pincel(self, seleccion: int) -> None:
        """Selecciona un pincel según el índice proporcionado.

        Args:
            seleccion (int): El índice del pincel seleccionado.
        """
        self.herramienta_seleccionada = DrawingStrategies.STRATEGIES[seleccion]
        print(f"{Texts.SELECT_TOOL} {self.herramienta_seleccionada}")

    def _actualizar_tamanho(self, valor: float) -> None:
        """Actualiza el tamaño del pincel según el valor del slider.

        Args:
            valor (float): El nuevo tamaño del pincel en forma de número flotante.
        """
        self.tamanho_pincel = int(valor)  # Actualiza el tamaño del pincel
        self.label_tamanho.configure(
            text=f"{Texts.SELECT_SIZE} {self.tamanho_pincel}"
        )  # Actualiza la etiqueta

    ########### Métodos de manipulación de figuras ###########

    def _borrar_figura(self) -> None:
        """Borra la figura seleccionada al hacer clic sobre ella."""
        print(Texts.SHAPE_CLEAR)

    def _borrar_todo(self) -> None:
        """Borra todas las figuras del lienzo."""
        print(Texts.SHAPE_CLEAR_ALL)

    def _deshacer_accion(self) -> None:
        """Deshace la última acción realizada en el lienzo."""
        print(Texts.SHAPE_UNDO)

    def _agrupar_figuras(self) -> None:
        """Agrupa las figuras seleccionadas en un solo objeto."""
        print(Texts.SHAPE_GROUP)

    def _desagrupar_figuras(self) -> None:
        """Desagrupa las figuras agrupadas, si hay alguna."""
        print(Texts.SHAPE_UNGROUP)

    def _crear_menu_superior(self) -> None:
        pass

    def _crear_menu_herramientas(self) -> None:
        """
        Crea la estructura del menú de herramientas en la ventana principal.

        Este método configura la interfaz de usuario dividiendo la ventana en dos secciones:
        - Un área de trabajo (canvas) a la izquierda donde se realizarán los dibujos.
        - Una columna de opciones (botones y controles) a la derecha, donde el usuario podrá
        seleccionar diferentes herramientas, colores y realizar acciones sobre el lienzo.

        Se organizan las siguientes secciones en el menú de herramientas:
        - Opciones de Pincel
        - Borradores
        - Selección de Colores
        - Agrupamiento de Figuras
        - Área de Salida de Texto
        """
        # Crear el frame izquierdo para el área de contenido
        self.frame_area_dibujo = self._crear_frame_izquierdo(self._ventana)

        # Crear el frame derecho para los botones
        frame_panel_opciones = self._crear_frame_derecho(self._ventana)

        # Configurar la proporción de la cuadrícula
        self._configurar_grid(self._ventana)

        # Crear el canvas en el frame izquierdo
        self._lienzo = self._crear_canvas(self.frame_area_dibujo)

        # Crear las barras de desplazamiento
        scrollbar_x = ctk.CTkScrollbar(
            self.frame_area_dibujo,
            orientation=ctk.HORIZONTAL,
            command=self._lienzo.xview,
        )
        scrollbar_x.grid(
            row=2, column=0, padx=0, pady=0, sticky="ew"
        )  # Barra en la parte inferior (horizontal)

        scrollbar_y = ctk.CTkScrollbar(
            self.frame_area_dibujo, orientation=ctk.VERTICAL, command=self._lienzo.yview
        )
        scrollbar_y.grid(
            row=1, column=1, padx=0, pady=0, sticky="ns"
        )  # Barra en el lado derecho (vertical)

        # Configurar el canvas para usar las barras de desplazamiento
        self.lienzo.configure(
            xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set
        )

        # Configurar expansión del grid
        self.frame_area_dibujo.grid_rowconfigure(
            1, weight=1
        )  # Hacer que la fila del canvas se expanda
        self.frame_area_dibujo.grid_columnconfigure(
            0, weight=1
        )  # Hacer que la columna del canvas se expanda

        # Crear frames para las diferentes secciones de opciones en el frame derecho
        self._crear_seccion_opciones(Texts.SECTION_OPTIONS, frame_panel_opciones)
        self._crear_seccion_colores(Texts.SECTION_COLOR, frame_panel_opciones)
        self._crear_seccion_borradores(Texts.SECTION_CLEAR, frame_panel_opciones)
        self._crear_seccion_acciones(Texts.SECTION_ACTIONS, frame_panel_opciones)
        self._crear_seccion_agrupar(Texts.SECTION_GRUPO, frame_panel_opciones)
        self._crear_seccion_salida_texto(Texts.SECTION_TEXT, frame_panel_opciones)
        self._crear_seccion_ajustes(Texts.SECTION_SETTINGS, frame_panel_opciones)

    def _crear_frame_izquierdo(self, ventana) -> ctk.CTkFrame:
        """
        Crea y retorna el frame izquierdo para el área de contenido.

        Args:
            ventana (tk.Tk):
                La ventana principal de la aplicación.

        Returns:
            ctk.CTkFrame:
                El frame izquierdo configurado.
        """
        frame_area_dibujo = ctk.CTkFrame(ventana, corner_radius=10)
        frame_area_dibujo.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)

        # Título para el frame izquierdo
        titulo_area_dibujo = ctk.CTkLabel(
            frame_area_dibujo, text=Texts.LEFT_FRAME_LABEL, font=(self.fuente, 16)
        )
        titulo_area_dibujo.grid(
            row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew"
        )  # Ocupar el espacio horizontal

        return frame_area_dibujo

    def _crear_frame_derecho(self, ventana: ctk.CTkFrame) -> ctk.CTkScrollableFrame:
        """
        Crea y retorna el frame derecho para los botones.

        Args:
            ventana (tk.Tk):
                La ventana principal de la aplicación.

        Returns:
            ctk.CTkScrollableFrame:
                El frame derecho configurado.
        """
        frame_panel_opciones = ctk.CTkScrollableFrame(ventana, corner_radius=10)
        frame_panel_opciones.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Título para el frame derecho
        titulo_panel_opciones = ctk.CTkLabel(
            frame_panel_opciones, text=Texts.RIGHT_FRAME_LABEL, font=(self.fuente, 16)
        )
        titulo_panel_opciones.pack(pady=10)

        return frame_panel_opciones

    def _configurar_grid(self, ventana: ctk.CTkFrame) -> None:
        """
        Configura la proporción de la cuadrícula en la ventana principal.

        Args:
            ventana (tk.Tk):
                La ventana principal de la aplicación.
        """
        ventana.grid_rowconfigure(0, weight=1)
        ventana.grid_columnconfigure(0, weight=1)
        ventana.grid_columnconfigure(1, weight=1)

    def _crear_canvas(self, parent_frame) -> ctk.CTkCanvas:
        """
        Crea y retorna el canvas en el frame dado.

        Args:
            parent_frame (tk.Frame):
                Frame en el que se añadirá el canvas.

        Returns:
            ctk.CTkCanvas:
                El canvas configurado.
        """
        canvas_dibujo = ctk.CTkCanvas(
            parent_frame, highlightthickness=0, bg=Default.CANVAS_BACKGROUND_COLOR
        )
        canvas_dibujo.grid(
            row=1, column=0, padx=10, pady=10, sticky="nsew"
        )  # Ocupa el espacio restante

        return canvas_dibujo

    def _crear_seccion_opciones(self, titulo: str, parent_frame) -> None:
        """
        Crea la sección de opciones de pincel en el menú de herramientas.

        Args:
            titulo (str):
                Título de la sección, que describe el contenido de la misma.
            parent_frame (tk.Frame):
                Frame en el que se añadirá la sección de opciones.
            instance (object):
                Instancia de la clase que contiene métodos a usar.

        Esta sección incluye:
        - Un menú desplegable para seleccionar diferentes tipos de pincel.
        - Un control deslizante para ajustar el tamaño del pincel.
        - Una etiqueta que muestra el tamaño actual del pincel.
        """
        frame_opciones_pincel = self._crear_frame_seccion(parent_frame, titulo)

        # Opción de menú para seleccionar pincel
        seleccion_pincel = tk.StringVar(value=Default.DRAWING_TOOL_NAME)
        option_menu = ctk.CTkOptionMenu(
            frame_opciones_pincel,
            variable=seleccion_pincel,
            values=list(DrawingStrategies.STRATEGIES.keys()),
            width=200,
            height=30,
            anchor="center",
            command=self._seleccionar_pincel,
        )
        option_menu.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        # Slider para seleccionar tamaño de línea
        slider_tamanho = ctk.CTkSlider(
            frame_opciones_pincel,
            from_=1,
            to=100,
            number_of_steps=50,
            width=200,
            height=20,
            command=self._actualizar_tamanho,
        )
        slider_tamanho.set(Default.DRAWING_SIZE)
        slider_tamanho.grid(row=2, column=1, padx=(30, 0), pady=10, sticky="ew")

        # Etiqueta para mostrar tamaño de línea
        self.label_tamanho = ctk.CTkLabel(
            frame_opciones_pincel,
            text=f"{Texts.SECTION_OPTIONS_LINE} {slider_tamanho.get()}",
            font=self.fuente,
            width=150,
            height=20,
        )
        self.label_tamanho.grid(row=2, column=2, pady=5, padx=(0, 10), sticky="nsew")

        # Configurar peso de las columnas
        for i in range(3):
            frame_opciones_pincel.grid_columnconfigure(i, weight=1)
            
    def _crear_seccion_colores(self, titulo: str, parent_frame) -> None:
        """
        Crea la sección de selección de colores en el menú de herramientas.

        Args:
            parent_frame (tk.Frame):
                Frame en el que se añadirá la sección de colores.
            instance (object):
                Instancia de la clase que contiene métodos a usar.

        Esta sección incluye un botón que permite al usuario seleccionar un color
        para el pincel que utilizará en el lienzo.
        """
        frame_colores = self._crear_frame_seccion(parent_frame, titulo)

        # Botón para seleccionar color
        btn_seleccionar_color = ctk.CTkButton(
            frame_colores,
            text=Texts.SECTION_COLOR_SELECT,
            command=self._seleccionar_color,
        )
        btn_seleccionar_color.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # Configurar peso de la columna
        frame_colores.grid_columnconfigure(0, weight=1)

    def _crear_seccion_borradores(self, titulo: str, parent_frame) -> None:
        """
        Crea la sección de borradores en el menú de herramientas.

        Args:
            parent_frame (tk.Frame):
                Frame en el que se añadirá la sección de borradores.

        Esta sección incluye botones para realizar las siguientes acciones:
        - Borrar la última figura dibujada.
        - Borrar todas las figuras en el lienzo.
        - Deshacer la última acción realizada.
        """
        frame_borradores = self._crear_frame_seccion(parent_frame, titulo)

        # Botones para las acciones de borrado
        btn_borrar_todas_figuras = ctk.CTkButton(
            frame_borradores, text=Texts.SECTION_CLEAR_ALL, command=self._borrar_todo
        )
        btn_borrar_todas_figuras.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        btn_deshacer_accion = ctk.CTkButton(
            frame_borradores,
            text=Texts.SECTION_CLEAR_UNDO,
            command=self._deshacer_accion,
        )
        btn_deshacer_accion.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Configurar peso de las columnas
        for i in range(2):
            frame_borradores.grid_columnconfigure(i, weight=1)

    def _crear_seccion_acciones(self, titulo: str, parent_frame) -> None:
        """
        Crea la sección de acciones (borrar, cambiar color, mover) en el menú de herramientas.

        Args:
            parent_frame (tk.Frame): Frame en el que se añadirá la sección de acciones.
        """

        frame_acciones = self._crear_frame_seccion(parent_frame, titulo)

        # Botones de acción
        self.boton_borrar = ctk.CTkButton(
            frame_acciones,
            text=Texts.SECTION_ACTIONS_DELETE,
            command=lambda: self._seleccionar_accion(Texts.SECTION_ACTIONS_DELETE),
            fg_color=Color.GREEN,
        )
        self.boton_borrar.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.boton_cambiar_color = ctk.CTkButton(
            frame_acciones,
            text=Texts.SECTION_ACTIONS_CHANGE_COLOR,
            command=lambda: self._seleccionar_accion(
                Texts.SECTION_ACTIONS_CHANGE_COLOR
            ),
            fg_color=Color.LIGHT_LIGHT_GREY,
        )
        self.boton_cambiar_color.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Configurar peso de las columnas
        for i in range(2):
            frame_acciones.grid_columnconfigure(i, weight=1)

    def _seleccionar_accion(self, accion: str) -> None:
        """
        Cambia el estado de los botones según la acción seleccionada.

        Args:
            accion (str): La acción que se ha seleccionado.
        """
        # Cambiar el color de los botones según la acción seleccionada
        buttons = {
            Texts.SECTION_ACTIONS_DELETE: self.boton_borrar,
            Texts.SECTION_ACTIONS_CHANGE_COLOR: self.boton_cambiar_color,
        }

        for key, button in buttons.items():
            if key == accion:
                button.configure(fg_color=Color.GREEN)  # Color activo
            else:
                button.configure(fg_color=Color.LIGHT_LIGHT_GREY)  # Color inactivo

        # Lógica adicional para manejar la acción seleccionada
        self._accion = accion
        print(f"Acción seleccionada: {self._accion}")

    def _crear_seccion_agrupar(self, titulo: str, parent_frame) -> None:
        """
        Crea la sección para agrupar y desagrupar figuras en el menú de herramientas.

        Args:
            parent_frame (tk.Frame):
                Frame en el que se añadirá la sección de agrupamiento.
            instance (object):
                Instancia de la clase que contiene métodos a usar.

        Esta sección incluye botones para agrupar y desagrupar figuras seleccionadas
        en el lienzo.
        """
        frame_agrupar = self._crear_frame_seccion(parent_frame, titulo)
        
        self.btn_agrupar = ctk.CTkButton(
            frame_agrupar,
            text=Texts.SECTION_GRUPO_GROUP,
            command=self._seleccionar_agrupar,
        )
        self.btn_agrupar.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.btn_desagrupar = ctk.CTkButton(
            frame_agrupar,
            text=Texts.SECTION_GRUPO_UNGROUP,
            command=self._seleccionar_desagrupar,
        )
        self.btn_desagrupar.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        
        # Configurar peso de las columnas
        for i in range(2):
            frame_agrupar.grid_columnconfigure(i, weight=1)
    
    def _seleccionar_agrupar(self) -> None:
        """
        Selecciona la acción de agrupar las líneas o figuras seleccionadas.
        
        Este método se activa cuando el usuario elige agrupar elementos, 
        mostrando un mensaje de confirmación en la consola.
        """
        print("Acción seleccionada: Agrupar")

    def _seleccionar_desagrupar(self) -> None:
        """
        Selecciona la acción de desagrupar las figuras agrupadas previamente.
        
        Este método se activa cuando el usuario elige desagrupar, mostrando 
        un mensaje de confirmación en la consola.
        """
        print("Acción seleccionada: Desagrupar")


    def _crear_seccion_salida_texto(self, titulo: str, parent_frame) -> None:
        """
        Crea la sección de salida de texto en el menú de herramientas.

        Args:
            parent_frame (tk.Frame):
                Frame en el que se añadirá la sección de salida de texto.
            instance (object):
                Instancia de la clase que contiene métodos a usar.

        Esta sección incluye un área de texto donde se mostrará la salida de
        información o mensajes relacionados con las acciones realizadas en el lienzo,
        así como un botón para limpiar el área de texto.
        """
        frame_salida_texto = self._crear_frame_seccion(parent_frame, titulo)

        # Área de texto para mostrar salida
        self.area_texto = ctk.CTkTextbox(frame_salida_texto, width=200, height=100)
        self.area_texto.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Botón para limpiar el área de texto
        btn_limpiar = ctk.CTkButton(
            frame_salida_texto,
            text=Texts.SECTION_TEXT_CLEAR,
            command=self._limpiar_texto,
        )
        btn_limpiar.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Configurar peso de las columnas
        for i in range(2):
            frame_salida_texto.grid_columnconfigure(i, weight=1)

    def _limpiar_texto(self):
        """Limpia el texto del textbox."""
        self.area_texto.delete("1.0", ctk.END)  # Elimina todo el texto

    def _anadir_texto(self, texto):
        """Añade texto al textbox."""
        texto_a_anadir = f"{texto}\n"
        self.area_texto.insert(ctk.END, texto_a_anadir)  # Añade texto al final

    def _crear_seccion_ajustes(self, titulo: str, parent_frame) -> None:
        """
        Crea la sección de ajustes en el menú de herramientas.

        Args:
            titulo (str): El título de la sección.
            parent_frame (tk.Frame): El frame en el que se añadirá la sección de ajustes.
        """
        frame_ajustes = self._crear_frame_seccion(parent_frame, titulo)

        # Botón para resetear el zoom
        btn_reset_zoom = ctk.CTkButton(
            frame_ajustes, text=Texts.SECTION_SETTINGS_ZOOM, command=self._resetear_zoom
        )
        btn_reset_zoom.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # Botón para cerrar la aplicación
        btn_cerrar_app = ctk.CTkButton(
            frame_ajustes,
            text=Texts.SECTION_SETTINGS_EXIT,
            command=self._cerrar_aplicacion,
        )
        btn_cerrar_app.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Botón para mostrar atajos de teclado
        btn_atajos_teclado = ctk.CTkButton(
            frame_ajustes,
            text="Atajos de Teclado",
            command=self._mostrar_atajos_teclado,
        )
        btn_atajos_teclado.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Configurar peso de las columnas
        frame_ajustes.grid_columnconfigure(0, weight=1)
        frame_ajustes.grid_columnconfigure(1, weight=1)

    def _mostrar_atajos_teclado(self) -> None:
        """Abre una ventana con los atajos de teclado de la aplicación."""
        atajos_ventana = ctk.CTkToplevel(self._ventana)
        atajos_ventana.title("Atajos de Teclado")

        # Asegurar que la ventana se eleve por encima de la ventana principal
        atajos_ventana.lift()
        atajos_ventana.attributes('-topmost', True)
        # Crear un marco para el contenido
        frame_contenido = ctk.CTkFrame(atajos_ventana)
        frame_contenido.pack(padx=10, pady=10)

        # Texto con los atajos
        atajos_texto = """
        Atajos de Teclado:

        Ctrl + Z: Deshacer
        Esc: Cerrar ventana

        Click Izquierdo: Iniciar dibujo
        Click Derecho: Seleccionar línea
        Arrastrar: Dibujar en movimiento
        Rueda del ratón: Zoom
        Espacio: Realizar acción

        W: Mover arriba
        A: Mover izquierda
        S: Mover abajo
        D: Mover derecha
        Flechas: Mover canvas

        G: Agrupar figuras
        H: Desagrupar figuras
        """

        # Mostrar los atajos en un widget de texto
        texto_atajos = ctk.CTkTextbox(frame_contenido, height=360, width=300,font=(self.fuente, 14))
        texto_atajos.insert("0.0", atajos_texto)
        texto_atajos.configure(state="disabled")  # Hacerlo de solo lectura
        texto_atajos.pack()

        # Botón para cerrar la ventana de atajos
        btn_cerrar_atajos = ctk.CTkButton(atajos_ventana, text="Cerrar", command=atajos_ventana.destroy)
        btn_cerrar_atajos.pack(pady=(10, 0))  # Aumentar el espacio en la parte superior


    def _resetear_zoom(self) -> None:
        """Restablece el zoom a su valor predeterminado."""
        print("Resetear zoom")

    def _cerrar_aplicacion(self) -> None:
        """Cierra la aplicación."""
        self._ventana.quit()  # Método para cerrar la ventana

    def _crear_frame_seccion(self, parent_frame, titulo: str) -> ctk.CTkFrame:
        """
        Crea y retorna un frame para una sección del menú.

        Args:
            parent_frame (tk.Frame):
                Frame en el que se añadirá el nuevo frame.
            titulo (str):
                Título de la sección.

        Returns:
            ctk.CTkFrame:
                El frame de sección configurado.
        """
        frame_seccion = ctk.CTkFrame(
            parent_frame, corner_radius=10, fg_color=Color.LIGHT_GRAY
        )
        frame_seccion.pack(pady=10, padx=10, fill="x")

        # Título de la sección
        titulo_seccion = ctk.CTkLabel(frame_seccion, text=titulo, font=(self.fuente, 14))
        titulo_seccion.grid(row=0, column=0, pady=(10, 0), sticky="nsew", columnspan=3)

        # Línea separadora
        separator = ctk.CTkFrame(
            frame_seccion, height=2, corner_radius=10, fg_color=Color.GRAY
        )
        separator.grid(
            row=1, column=0, columnspan=3, pady=(10, 0), padx=20, sticky="ew"
        )

        return frame_seccion

    ########### Getters y setters ###########

    @property
    def color_seleccionado(self) -> str:
        """Devuelve el color seleccionado para dibujar."""
        return self._color_seleccionado

    @color_seleccionado.setter
    def color_seleccionado(self, color: str) -> None:
        """Establece el color seleccionado para dibujar."""
        self._color_seleccionado = color

    @property
    def herramienta_seleccionada(self) -> str:
        """Devuelve la herramienta seleccionada para dibujar."""
        return self._herramienta_seleccionada

    @herramienta_seleccionada.setter
    def herramienta_seleccionada(self, herramienta: AlgoritmoDibujo) -> None:
        """Establece la herramienta seleccionada para dibujar."""
        self._herramienta_seleccionada = herramienta

    @property
    def tamanho_pincel(self) -> int:
        """Devuelve el grosor del pincel utilizado para dibujar."""
        return self._tamanho_pincel

    @tamanho_pincel.setter
    def tamanho_pincel(self, tamanho: int) -> None:
        """Establece el grosor del pincel utilizado para dibujar."""
        self._tamanho_pincel = tamanho

    @property
    def lienzo(self) -> ctk.CTkCanvas:
        """Devuelve el lienzo donde se dibujan las figuras."""
        return self._lienzo

    @lienzo.setter
    def lienzo(self, lienzo: ctk.CTkCanvas) -> None:
        """Establece el lienzo donde se dibujan las figuras."""
        self._lienzo = lienzo
