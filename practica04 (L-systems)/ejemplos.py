class Ejemplos:

    SIERPINSKY = {
        "axioma": "A",
        "reglas": {"A": "B-A-B", "B": "A+B+A"},
        "angulo": 60,
        "punto_inicial": (0, 0),
        "rotacion": 0,
        "colormap": {"A": "#F2F2F2", "B": "#F8D79B"},  # Blanco y dorado pastel suave
    }

    CURVA_DRAGON = {
        "axioma": "FX",
        "reglas": {"X": "X+YF+", "Y": "-FX-Y"},
        "angulo": 90,
        "punto_inicial": (0, 0),
        "rotacion": 90,
        "colormap": {"F": "#FFEB99"},  # Amarillo pastel
    }

    ARBOL_FIBO = {
        "axioma": "X",
        "reglas": {"X": "F[+X]F[-X]+X", "F": "FF"},
        "angulo": 25,
        "punto_inicial": (0, 0),
        "rotacion": 90,
        "colormap": {"F": "#C8B59A", "X": "#A8D08D"},  # Tonos pastel árbol y hojas
    }

    LEVY_FLAKE = {
        "axioma": "F",
        "reglas": {"F": "+F--F+"},
        "angulo": 45,
        "punto_inicial": (0, 0),
        "rotacion": 0,
        "colormap": {"F": "#A8D8E8"},  # Azul hielo pastel
    }

    CURVA_KOCH = {
        "axioma": "F",
        "reglas": {"F": "F+F-F-F+F"},
        "angulo": 90,
        "punto_inicial": (0, 0),
        "rotacion": 0,
        "colormap": {"F": "#9B4D96"},  # Morado neón
    }

    HILBERT_SERPIENTE = {
        "axioma": "X",
        "reglas": {"X": "+YF-XFX-FY+", "Y": "-XF+YFY+FX-"},
        "angulo": 90,
        "punto_inicial": (0, 0),
        "rotacion": 0,
        "colormap": {"F": "#B6E7B1"},  # Verde pastel
    }

    OPCIONES = [
        "Sierpinski",
        "Curva Dragon",
        "Arbol Fibo",
        "Levy Flake",
        "Curva Koch",
        "Hilbert Serpiente",
    ]

    EJEMPLOS_LSYSTEM = {
        "Sierpinski": SIERPINSKY,
        "Curva Dragon": CURVA_DRAGON,
        "Arbol Fibo": ARBOL_FIBO,
        "Levy Flake": LEVY_FLAKE,
        "Curva Koch": CURVA_KOCH,
        "Hilbert Serpiente": HILBERT_SERPIENTE,
    }
