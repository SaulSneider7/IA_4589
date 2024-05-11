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

# Recompensas - Elige un laberinto para utilizarlo
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
def fin_del_juego(fila_actual, columna_actual):
    if recompensas[fila_actual, columna_actual] == -1.:
        return False
    else:
        return True


def punto_inicial():
    while True:
        fila_actual = np.random.randint(filas)
        columna_actual = np.random.randint(columnas)

        if not fin_del_juego(fila_actual, columna_actual):
            break

    return fila_actual, columna_actual


def punto_siguiente(fila_actual, columna_actual, indice_de_accion):
    nueva_fila = fila_actual
    nueva_columna = columna_actual

    acciones = ['arriba', 'derecha', 'abajo', 'izquierda']

    if acciones[indice_de_accion] == 'arriba' and fila_actual > 0:
        nueva_fila -= 1
    elif acciones[indice_de_accion] == 'derecha' and columna_actual < columnas - 1:
        nueva_columna += 1
    elif acciones[indice_de_accion] == 'abajo' and fila_actual < filas - 1:
        nueva_fila += 1
    elif acciones[indice_de_accion] == 'izquierda' and columna_actual > 0:
        nueva_columna -= 1

    return nueva_fila, nueva_columna


# -------------------------------------------------------------------------
# Sesión 3: Entrenamiento

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

# Entrena tu inteligencia artificial haciendo que resuelva el laberinto 1000 veces
for episode in range(1000):
    x, y = punto_inicial()

    while True:
        x_anterior = x
        y_anterior = y

        accion = siguiente_accion(x, y, exploracion)

        # Calcular siguiente punto
        x, y = punto_siguiente(x, y, accion)

        # Obtener valor q actual para esa accion en la posición anterior
        valor_q_actual = valores_q[x_anterior, y_anterior, accion]

        # Calcular nuevo valor q
        recompensa = recompensas[x, y]
        temporal_difference = recompensa + (descuento * np.max(valores_q[x, y, :])) - valor_q_actual
        nuevo_valor_q = valor_q_actual + (aprendizaje * temporal_difference)

        # Actualizar nuevo valor q
        valores_q[x_anterior, y_anterior, accion] = nuevo_valor_q
        # Espera y fondo
        ventana.fill((0, 0, 0))

        # Diujar laberinto
        dibujar_laberinto(x, y)
        pygame.display.flip()

        # Condición del fin del juego
        if fin_del_juego(x, y):
            if recompensas[x, y] == 100:
                print("¡Has ganado!")
            else:
                print("¡Has perdido!")
            break

print('¡Entrenamiento completado!')


# -------------------------------------------------------------------------
# Sesión 4 - Resultados del entrenamiento

# Define una función que va a elegir siempre el camino más corto entre un punto inicial y la meta
def camino_mas_corto(inicio_x, inicio_y):
    # No continuar si el punto inicial no es válido
    if fin_del_juego(inicio_x, inicio_y):
        return []

    # Empezar a guardar el camino
    fila_actual, columna_actual = inicio_x, inicio_y
    camino = [[fila_actual, columna_actual]]

    # Continua buscando el siguiente paso hasta llegar a la meta.
    while not fin_del_juego(fila_actual, columna_actual):
        # Obten de la tabla q la mejor acción posible para dicha posicion
        accion_actual = siguiente_accion(fila_actual, columna_actual, 0.)

        # Muevete a la siguigiente posicición
        fila_actual, columna_actual = punto_siguiente(fila_actual, columna_actual, accion_actual)

        # Guarda el valor el nuevo valor en el arreglo
        camino.append([fila_actual, columna_actual])

    # Regresa el camino completo de la posición inicial a la meta
    return camino


# Dibuja el camino más corto desde una posición hasta la meta
def dibuja_camino_mas_corto(inicio_x, inicio_y):
    # Obten el camino más corto
    camino = camino_mas_corto(inicio_x, inicio_y)

    # Dibuja posición por posición el camino más corto
    for i, j in camino:
        dibujar_laberinto(i, j)
        ventana.fill((0, 0, 0))
        dibujar_laberinto(i, j)
        pygame.display.flip()
        sleep(0.1)


# Prueba tu inteligencia artificial para resolver el laberinto desde varias posiciones iniciales
for ejemplo in range(3):
    x, y = punto_inicial()
    dibuja_camino_mas_corto(x, y)


# -------------------------------------------------------------------------
# No borres esta linea, deja esto siempre hasta el final
# Cierra el juego
pygame.quit()