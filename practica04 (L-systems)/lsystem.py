import turtle
import math


class LSystem:
    def __init__(self, axiom, rules, angle=90, length=10, iterations=5, start_point=(0, 0), start_angle=0, rotation_offset=0, color_map = {}):
        self.axiom = axiom
        self.rules = rules
        self.angle = angle
        self.length = length
        self.iterations = iterations
        self.start_point = start_point
        self.start_angle = start_angle
        self.rotation_offset = rotation_offset
        self.color_map = color_map  # Mapeo de colores para cada variable

    def generate(self):
        result = self.axiom
        for _ in range(self.iterations):
            result = ''.join(self.rules.get(c, c) for c in result)
        return result

    def calculate_bounds(self):
        """Calcula los límites del dibujo para centrarlo."""
        x, y = 0, 0
        min_x, min_y = 0, 0
        max_x, max_y = 0, 0
        angle = math.radians(self.start_angle + self.rotation_offset)
        stack = []

        for char in self.generate():
            if char in "ABCDEF":  # Avanzar
                x += self.length * math.cos(angle)
                y += self.length * math.sin(angle)
                min_x, max_x = min(min_x, x), max(max_x, x)
                min_y, max_y = min(min_y, y), max(max_y, y)
            elif char == '+':  # Girar a la derecha
                angle -= math.radians(self.angle)
            elif char == '-':  # Girar a la izquierda
                angle += math.radians(self.angle)
            elif char == '[':  # Guardar estado
                stack.append((x, y, angle))
            elif char == ']':  # Restaurar estado
                x, y, angle = stack.pop()

        return min_x, max_x, min_y, max_y
    
    def draw(self, velocidad, instantaneo):
        turtle.mode('logo')
        turtle.clearscreen()
        turtle.tracer(False)
        turtle.update()

        def draw_turtle():
            screen = turtle.Screen()
            screen.bgcolor("#1E1E1E")
            screen.screensize(1000, 1000)
            
            # Calcular límites y ajustar el sistema de coordenadas
            min_x, max_x, min_y, max_y = self.calculate_bounds()
            padding = self.length * 2  # Espaciado adicional para mejor visualización
            screen.setworldcoordinates(
                min_x - padding, min_y - padding, max_x + padding, max_y + padding
            )

            pen = turtle.Turtle()
            pen.speed(velocidad)
            pen.hideturtle()

            # Configuración inicial de la tortuga con rotación personalizada
            pen.penup()
            pen.setpos(self.start_point)
            pen.setheading(self.start_angle + self.rotation_offset)
            pen.pendown()

            if instantaneo:
                turtle.tracer(0, 0)
            else:
                turtle.tracer(1, 10)

            stack = []
            for char in self.generate():
                # Verificar si la ventana sigue activa
                try:
                    # Usar winfo_exists() en el objeto Screen
                    if not turtle.getcanvas().winfo_exists():  
                        print("La ventana fue cerrada durante la ejecución.")
                        turtle.bye()  # Cerrar correctamente la ventana de turtle
                        return  # Salir del ciclo y de la función de dibujo
                except turtle.Terminator:
                    # Si turtle se detiene o la ventana es cerrada
                    print("La ventana de Turtle fue cerrada manualmente. El dibujo ha terminado.")
                    turtle.bye()  # Cerrar correctamente la ventana de turtle
                    return

                if char in self.color_map:  # Cambiar color para las variables definidas
                    pen.pencolor(self.color_map[char])
                    pen.forward(self.length)
                elif char == '+':  # Girar a la derecha
                    pen.right(self.angle)
                elif char == '-':  # Girar a la izquierda
                    pen.left(self.angle)
                elif char == '[':  # Guardar estado
                    stack.append((pen.pos(), pen.heading()))
                elif char == ']':  # Restaurar estado
                    pos, heading = stack.pop()
                    pen.penup()
                    pen.setpos(pos)
                    pen.setheading(heading)
                    pen.pendown()
                elif char == '|':  # Giro de 180 grados
                    pen.right(180)
                elif char == '&':  # Giro antihorario
                    pen.left(self.angle)
                elif char == '^':  # Giro horario
                    pen.right(self.angle)
                elif char == '\\':  # Giro de 45 grados
                    pen.left(45)
                elif char == '/':  # Giro de -45 grados
                    pen.right(45)
                elif char == 'G':  # Sin movimiento
                    pass
                else:
                    # Ignorar caracteres desconocidos
                    # print(f"Caracter desconocido: {char}")
                    pass

            if instantaneo:
                turtle.update()
            screen.exitonclick()

        try:
            draw_turtle()
        except turtle.Terminator:
            print("La ventana de Turtle fue cerrada manualmente. El dibujo ha terminado.")
            turtle.bye()  # Cerrar correctamente la ventana de turtle


# Ejemplo de uso
if __name__ == "__main__":
    axiom = "A"
    rules = {"A": "F+[[A]-A]-F[-FA]+A", "F": "FF"}
    start_point = (0, 0)  # Punto de inicio personalizado
    start_angle = 0  # Ángulo inicial
    rotation_offset = 90  # Offset de rotación adicional
    color_map = {"A": "red", "F": "blue"}
    # Crear el L-System y definir el mapeo de colores
    lsystem = LSystem(axiom, rules, angle=25, length=10, iterations=4, start_point=start_point, start_angle=start_angle, rotation_offset=rotation_offset, color_map=color_map)

    # Dibujar el sistema
    lsystem.draw(velocidad=0, instantaneo=False)
