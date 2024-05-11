# -------------------------------------------------------------------------
# Crack the Code
# Aprendizaje por reforzamiento
# -------------------------------------------------------------------------
# Importar bibliotecas que se utilizarán - no modifiques esta sección
import pygame
from pygame.locals import *
import numpy as np
from time import sleep
import laberintos

# -------------------------------------------------------------------------
# Sesión 1: Laberintos, acciones y recompensas

# Recompensas y tamaño del laberinto
# Escribe aquí tu código
recompensas = laberintos.laberinto_1
filas = recompensas.shape[0]
columnas = recompensas.shape[1]

size = 32
ventana_alto = columnas * size
ventana_ancho = filas * size

pygame.init()
ventana = pygame.display.set_mode((ventana_alto, ventana_ancho), pygame.HWSURFACE)

img_muro = pygame.image.load("Imagenes/Muro.jpg").convert()
img_jugador = pygame.image.load("Imagenes/Jugador.jpg").convert()
img_meta = pygame.image.load("Imagenes/Meta.jpg").convert()

# Función para dibujar el estado actual del laberinto y la posición del jugador
def dibujar_laberinto(jugador_x, jugador_y):
    for i in range(0, recompensas.shape[0]):
        for j in range(0, recompensas.shape[1]):
            if recompensas[i, j] == -100:
                ventana.blit(img_muro, (j * size, i * size))
            if recompensas[i, j] == 100:
                ventana.blit(img_meta, (j * size, i * size))
    ventana.blit(img_jugador, (jugador_y * size, jugador_x * size))


# -------------------------------------------------------------------------
# Sesión 2: Fin del juego, punto inicial y punto siguiente

# Define la condición final
# Si la recompensa es -1 (es una casilla vacia) entonces el juego sigue
# Si choca con un muro (pierde) o llega a la meta (gana) el juego termina
def fin_del_juego(fila_actual, columna_actual):
    if recompensas [fila_actual, columna_actual] == -1:
        return False
    else:
        return True


# Inicia el juego desde una posición aleatoria
def punto_inicial():
    while True:
        fila_actual = np.random.randint(filas)
        columna_actual = np.random.randint(columnas)

        if not fin_del_juego(fila_actual, columna_actual):
            break
    
    return fila_actual, columna_actual

# Esta función nos ayuda a elegir una acción facilmente y calcular la nueva posición utilizando solo un numero
def punto_siguiente(fila_actual, columna_actual, indice_de_accion):
    nueva_fila = fila_actual
    nueva_columna = columna_actual

    acciones = ['arriba', 'abajo', 'izquierda', 'derecha']

    if acciones[indice_de_accion] == 'arriba' and fila_actual > 0:
        nueva_fila -= 1
    elif acciones[indice_de_accion] == 'derecha' and columna_actual < columnas - 1:
        nueva_columna += 1
    elif acciones[indice_de_accion] == 'abajo' and fila_actual < filas - 1:
        nueva_fila += 1
    elif acciones[indice_de_accion] == 'izquierda' and columna_actual > 0:
        nueva_columna -= 1

    return fila_actual, columna_actual

# -------------------------------------------------------------------------
# Sesión 3: Entrenamiento

# Tabla con los valores Q y parametros del entrenamiento
# Escribe aquí tu codigo
valores_q = np.zeros((filas, columnas, 4))

exploracion = 0.1
descuento = 0.9
aprendizaje = 0.9


def siguiente_accion(fila_actual, columna_actual, explorar):
    if np.random.random() > explorar:
        return np.argmax(valores_q[fila_actual, columna_actual])
    else:
        return np.random.randint(4)


# -------------------------------------------------------------------------
# JUEGO - Este parte del código se modificará sesión a sesión

# Escribe tu codigo aquí
for episode in range(1000):
    x, y = punto_inicial()

    while True:
        x_anterior = x
        y_anterior = y

        accion = siguiente_accion(x, y, exploracion)

        x,y = punto_siguiente(x, y, accion)

        valor_q_actual = valores_q[x_anterior, y_anterior, accion]

        recompensa = recompensas[x, y]
        temporal_difference = recompensa + (descuento * np.max(valores_q[x, y, :])) - valor_q_actual
        nuevo_valor_q = valor_q_actual + (aprendizaje * temporal_difference)

        valores_q[x_anterior, y_anterior, accion] = nuevo_valor_q
        ventana.fill((0, 0, 0))

        dibujar_laberinto(x, y)
        pygame.display.flip()

        if fin_del_juego(x, y):
            if recompensas[x, y] == 100:
                print("Ganaste")
            else:
                print("Perdiste")
            break
        
print('Entrenamiento completado')
# -------------------------------------------------------------------------
# Sesión 4 - Resultados del entrenamiento

# Define una función que va a elegir siempre el camino más corto entre un punto inicial y la meta
def camino_mas_corto(inicio_x, inicio_y):
    # Escribe aquí tu codigo
    pass


# Dibuja el camino más corto desde una posición hasta la meta
def dibuja_camino_mas_corto(inicio_x, inicio_y):
    # Escribe aquí tu codigo
    pass


# Prueba tu inteligencia artificial para resolver el laberinto desde varias posiciones iniciales
# Escribe aquí tu codigo


# -------------------------------------------------------------------------
# No borres esta linea, deja esto siempre hasta el final
# Cierra el juego
pygame.quit()
