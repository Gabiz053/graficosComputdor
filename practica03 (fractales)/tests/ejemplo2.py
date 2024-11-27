import pygame
import numpy as np

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 800
MAX_ITER = 256
zoom_factor = 1.0
pan_x, pan_y = 0.0, 0.0

# Función para calcular el conjunto de Mandelbrot
def mandelbrot(c, max_iter):
    z = c
    for i in range(max_iter):
        if abs(z) > 2:
            return i
        z = z*z + c
    return max_iter

# Generar la imagen del conjunto de Mandelbrot
def generate_mandelbrot(xmin, xmax, ymin, ymax, width, height, max_iter):
    x, y = np.linspace(xmin, xmax, width), np.linspace(ymin, ymax, height)
    image = np.zeros((height, width))

    for i in range(height):
        for j in range(width):
            c = complex(x[j], y[i])
            image[i, j] = mandelbrot(c, max_iter)
    
    return image

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fractal de Mandelbrot")

# Definir la región inicial del conjunto de Mandelbrot
xmin, xmax = -2.0, 1.0
ymin, ymax = -1.5, 1.5

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Rueda del ratón hacia arriba (zoom in)
                zoom_factor *= 1.2
            elif event.button == 5:  # Rueda del ratón hacia abajo (zoom out)
                zoom_factor /= 1.2
        elif event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:  # Arrastrar para mover el fractal
                mx, my = event.pos
                pan_x += (mx - WIDTH // 2) * 0.005
                pan_y += (my - HEIGHT // 2) * 0.005

    # Calcular los nuevos límites del conjunto de Mandelbrot basado en el zoom
    center_x = (xmin + xmax) / 2
    center_y = (ymin + ymax) / 2
    width_span = (xmax - xmin) / zoom_factor
    height_span = (ymax - ymin) / zoom_factor

    xmin = center_x - width_span / 2 + pan_x
    xmax = center_x + width_span / 2 + pan_x
    ymin = center_y - height_span / 2 + pan_y
    ymax = center_y + height_span / 2 + pan_y

    # Generar la nueva imagen del fractal
    image = generate_mandelbrot(xmin, xmax, ymin, ymax, WIDTH, HEIGHT, MAX_ITER)

    # Convertir la imagen a una superficie de Pygame
    surface = pygame.surfarray.make_surface(np.uint8(image * 255 / MAX_ITER))

    # Dibujar en la pantalla
    screen.blit(surface, (0, 0))
    pygame.display.flip()

# Finalizar Pygame
pygame.quit()
