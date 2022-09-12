import librerias
import globales



#panel grafico

print("╔═══════════════════════════════════════╗")	
print("║Ingrese la dificultad del juego:       ║\n",end="")
print("║FACIL    ",end="                              ║\n")
print("║MEDIO    ",end="                              ║\n")
print("║DIFICIL    ",end="                            ║\n")
print("╚═══════════════════════════════════════╝")





#opcion de dificultad

dificultad = input("Dificultad: ")
dificultad = dificultad.upper()

dificultades = ["FACIL","MEDIO","DIFICIL"]
tamanios     = ["6x6","8x8"]

while(dificultad not in dificultades):
	dificultad = input("Dificultad: ").upper()

if(dificultad == "FACIL"):

    profundidad = 3

elif(dificultad == "MEDIO"):

    profundidad = 5

elif (dificultad == "DIFICIL"):

    profundidad = 8   


PROFUNDIDAD_IA = profundidad



#opcion de tamaño

tamanio = input("Ingrese tamaño puede ser 6x6 o 8x8: ")
tamanio = tamanio.lower()


while(tamanio not in tamanios):
	tamanio = input("Tamano: ").lower()

if(tamanio == "8x8"):
	globales.tam_tablero = 8

if(tamanio == "6x6"):
	globales.tam_tablero = 6

librerias.os.system("cls")



def DIBUJO_REVERSI():	
	print("╔═══════════════════════════════════════╗")
	print("║                                    _  ║\
		 \n║                                   (_) ║\
		 \n║  _ __  ___ __   __ ___  _ __  ___  _  ║\
		 \n║ | '__|/ _ \\\ \ / // _ \| '__|/ __|| | ║\
		 \n║ | |  |  __/ \ V /|  __/| |   \__ \| | ║\
		 \n║ |_|   \___|  \_/  \___||_|   |___/|_| ║")
	print("║                                       ║")
	print("║                                       ║")
	print("╚═══════════════════════════════════════╝")	





def leer_tablero():
    tablero = librerias.np.zeros((globales.tam_tablero,globales.tam_tablero))
    iconos_tablero = {
        '▀': globales.BLANCAS,
        'N': globales.NEGRAS,
        '•': globales.NADA
    }
    i = 0  # fila
    for linea in librerias.sys.stdin:
        for j in range(globales.tam_tablero):
            tablero[i][j] = iconos_tablero.get(linea[j], globales.NADA) # quietly ignore bad chars
        i += 1
    return tablero



#esta funcion busca al ganador lo unico que hace es contar la cantidad de fichas del tablero y
#ver cual es mayor y entrega al ganador
def buscar_ganador(tablero):
    white_count = librerias.np.count_nonzero(tablero == globales.BLANCAS)
    black_count = librerias.np.count_nonzero(tablero == globales.NEGRAS)
    if white_count > black_count:
        return globales.BLANCAS
    elif white_count < black_count:
        return globales.NEGRAS
    return globales.EMPATE



#esta funcion sirve para saber cuantas fichas hay en el tablero en todo momento
def contar_fichas(tablero):

    white_count = librerias.np.count_nonzero(tablero == globales.BLANCAS)
    black_count = librerias.np.count_nonzero(tablero == globales.NEGRAS)

    print("╔═══════════════════════════════════════╗")
    print("║Fichas blancas║Fichas negras║Dificultad║")
    print("      ",white_count,"           ",black_count,"        ", dificultad)
    print("╚",end="══════════════╩═════════════╩══════════╝\n")

    return ""



def REVISAR_MOV_VALIDOS(tablero, TURNO_BLANCAS):
    mov_validos = []
    for i in range(globales.tam_tablero):
        for j in range(globales.tam_tablero):
            if tablero[i][j] != globales.NADA:
                continue   
            if SE_PUEDE_CAPTURAR(tablero, i, j, TURNO_BLANCAS):
                mov_validos.append((i,j))
    return mov_validos



# con la funcion SE_PUEDE_CAPTURAR logramos verificar si la pieza en la posicion señalada
#tiene el color contrario o si no hay
def SE_PUEDE_CAPTURAR(tablero, i, j, TURNO_BLANCAS):
    for ifila, jcol in globales.COORDENADAS:
        if CONDICIONES_CAPTURA(tablero, i, ifila, j, jcol, TURNO_BLANCAS):
            return True
    return False



#Verifica si se puede hacer una captura modificando fila y col
#cuando encuentra una pieza aliada devuelve true si llega al final del tablero o es enemiga muestra falso
def CONDICIONES_CAPTURA(tablero, fila, fd, col, cd, TURNO_BLANCAS):
    if (fila+fd < 0) or (fila+fd >= globales.tam_tablero):
        return False
    if (col+cd < 0) or (col+cd >= globales.tam_tablero):
        return False

    enemy_color = globales.NEGRAS if TURNO_BLANCAS else globales.BLANCAS
    if tablero[fila+fd][col+cd] != enemy_color:
        return False

    friendly_color = globales.BLANCAS if TURNO_BLANCAS else globales.NEGRAS
    scan_row = fila + 2*fd 
    scan_col = col + 2*cd 
    while (scan_row >= 0) and (scan_row < globales.tam_tablero) and (scan_col >= 0) and (scan_col < globales.tam_tablero):
        if tablero[scan_row][scan_col] == globales.NADA:
            return False
        if tablero[scan_row][scan_col] == friendly_color:
            return True
        scan_row += fd
        scan_col += cd
    return False



#con la funcion CAPTURAR usamos la funcion anterior para finalmente cambiar el tablero y mostrar
#como queda luego de una captura modificando la copia del tablero
def CAPTURAR(tablero, fila, col, TURNO_BLANCAS):
    enemy_color = globales.NEGRAS if TURNO_BLANCAS else globales.BLANCAS
    for fd, cd in globales.COORDENADAS:
        if CONDICIONES_CAPTURA(tablero, fila, fd, col, cd, TURNO_BLANCAS):
            flip_row = fila + fd
            flip_col = col + cd
            while tablero[flip_row][flip_col] == enemy_color:
                tablero[flip_row][flip_col] = -enemy_color
                flip_row += fd
                flip_col += cd
    return tablero


#Con esta funcion creamos una copia del tablero para que se pueda interactuar de forma visual
def REALIZAR_MOV(tablero, move, TURNO_BLANCAS):
    tablero_n = librerias.copy.deepcopy(tablero)
    tablero_n[move[0]][move[1]] = globales.BLANCAS if TURNO_BLANCAS else globales.NEGRAS
    tablero_n = CAPTURAR(tablero_n, move[0], move[1], TURNO_BLANCAS)
    return tablero_n

# REVISAR_GANADOR como su nombre lo indica busca quien gano o si hubo empate
def REVISAR_GANADOR(tablero):
    blancas_mov_validos = REVISAR_MOV_VALIDOS(tablero, True)
    if blancas_mov_validos:  
        return globales.NADA
    negras_mov_validos = REVISAR_MOV_VALIDOS(tablero, False)
    if negras_mov_validos:
        return globales.NADA
    # I guess the game's over
    return buscar_ganador(tablero)


# minimax:  aca asumimos que MAX son las blancas y MIN son las negras
# alpha y beta se utilizan para agregar limite y poder reducir la cantidad de nodos evaluados

camino = []

def minimax(tablero, TURNO_BLANCAS, busqueda_profundidad, alpha, beta):


    if busqueda_profundidad == 0:
        return librerias.np.count_nonzero(tablero == globales.BLANCAS) - librerias.np.count_nonzero(tablero == globales.NEGRAS)
    estado = REVISAR_GANADOR(tablero)
    if estado == globales.EMPATE:
        return 0
    if estado == globales.BLANCAS:
        return globales.VALOR_GANADOR
    if estado == globales.NEGRAS:
        return -globales.VALOR_GANADOR
    else:
        pass #Este pass sirve en caso de que no encuentre ninguna condicion de las anteriores para ganar
    


    if TURNO_BLANCAS:
        puntajemax = -1000
        mov_validos = REVISAR_MOV_VALIDOS(tablero, True)

        if len(mov_validos) == 0:
            puntajemax = minimax(tablero, False, busqueda_profundidad, alpha, beta)

        else:
            for move in mov_validos:
                tablero_n = REALIZAR_MOV(tablero, move, True) # Get the new tablero estado
                score = minimax(tablero_n, False, busqueda_profundidad - 1, alpha, beta)
                puntajemax = max(puntajemax, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break

        camino.append(1)

        return puntajemax
    

    else:
        puntajemin=  1000
        mov_validos = REVISAR_MOV_VALIDOS(tablero, False)

        if len(mov_validos) == 0:
            puntajemin = minimax(tablero, True, busqueda_profundidad, alpha, beta)
        
        else:
            for move in mov_validos:
                tablero_n = REALIZAR_MOV(tablero, move, False) # Get the new tablero estado
                score = minimax(tablero_n, True, busqueda_profundidad - 1, alpha, beta)
                puntajemin = min(puntajemin, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
        return puntajemin
    

# esta funcion es simple se encarga de imprimir un tablero
def DIBUJAR_TABLERO(tablero):
    iconos = {
        -1: " N ",0: " • ",1: " ▀ "}
        
    for i in range(globales.tam_tablero):
        linea = " "
        for j in range(globales.tam_tablero):
            linea += iconos[tablero[i][j]]
        print(linea)





# esta es la funcion donde ejecutaremos el juego donde la IA ya resivira la primera jugada por 
# default para que el jugador responda como las piezas negras
def REVERSI():
    tablero = POSICIONES_INICIO_TAB(globales.tam_tablero)
    while REVISAR_GANADOR(tablero) == globales.NADA:
        mov_validos = REVISAR_MOV_VALIDOS(tablero, True)
        if mov_validos: 
            print("IA")
            librerias.time.sleep(0.5)
            print("...")
            librerias.time.sleep(1)
            print("...")
            print("\n")
            best_val = float("-inf")
            best_move = None
            tiempo = librerias.time.time()
            for m in mov_validos:
                tablero_n = REALIZAR_MOV(tablero, m, True)
                mov_v = minimax(tablero_n, True, PROFUNDIDAD_IA, float("-inf"), float("inf"))
                if mov_v > best_val:
                    best_move = m
                    best_val = mov_v

            final = librerias.time.time()

            print("tiempo de espera de IA: ",final-tiempo)
            print("\n")
            tablero = REALIZAR_MOV(tablero, best_move, True)
            DIBUJO_REVERSI()
            print("\n")
            DIBUJAR_TABLERO(tablero)
            print("\n")
            print(contar_fichas(tablero))
            print("\n")            
            print("PROFUNDIDAD DE BUSQUEDA",len(camino))
            print("\n")            
            print("buscando movimientos posibles...")
            librerias.time.sleep(1)
            print("...")
            print("\n")
        
        else:
            print("LAS BLANCAS NO TIENEN MOVIMIENTOS LEGALES. Saltando...")
        

        mov_validos = REVISAR_MOV_VALIDOS(tablero, False)
        if mov_validos:
            mov_jugador = MOV_JUGADOR(tablero, mov_validos)
            tablero = REALIZAR_MOV(tablero, mov_jugador, False)
            DIBUJAR_TABLERO(tablero)
            print("\n")
        else:
            print("LAS NEGRAS NO TIENEN MOVIMIENTOS LEGALES. Saltando...")
        
        librerias.os.system("cls")
        camino.clear()
        DIBUJAR_TABLERO(tablero)
        print(contar_fichas(tablero))
    winner = buscar_ganador(tablero)
    if winner == globales.BLANCAS:
        print("GANAN LAS BLANCAS")
    elif winner == globales.NEGRAS:
        print("GANAN LAS NEGRAS")
    else:
        print("EMPATE")

def POSICIONES_INICIO_TAB(tam):

    if tam == 8:
        tablero = librerias.np.zeros((globales.tam_tablero, globales.tam_tablero))
        tablero[3][3] = globales.BLANCAS
        tablero[3][4] = globales.NEGRAS
        tablero[4][3] = globales.NEGRAS
        tablero[4][4] = globales.BLANCAS
    elif tam == 6:        
        tablero = librerias.np.zeros((globales.tam_tablero, globales.tam_tablero))
        tablero[2][2] = globales.BLANCAS
        tablero[2][3] = globales.NEGRAS
        tablero[3][2] = globales.NEGRAS
        tablero[3][3] = globales.BLANCAS

    return tablero


# Esta funcion sirve para mostrarle al jugador las jugadas validas en el tablero
# con posiciones faciles para no tener que introducir cordenadas 
# solo con numeros del 0 al numero de mov posibles
def MOV_JUGADOR(tablero, mov_validos):
    for i in range(globales.tam_tablero):
        linea = " "
        for j in range(globales.tam_tablero):
            if tablero[i][j] == globales.BLANCAS:
                linea += "▀"
            elif tablero[i][j] == globales.NEGRAS:
                linea += "N"
            else:
                if (i,j) in mov_validos:
                    linea += str(mov_validos.index((i,j))) # este index es para agruprarlos de forma que podamos conseguir las posiciones como numeros en vez de coordenadas
                else:
                    linea += "•"
        print(linea)
    while True:
        # entra en bucle hasta que encuentre un valor valido para mostrar
        print("\n")
        opcion = input("Eliga su movimiento entre [0-" + str(len(mov_validos)-1) + "]")
        try:
            movimiento_int = int(opcion)
            if movimiento_int >= 0 and movimiento_int < len(mov_validos):
                return mov_validos[movimiento_int]
            else:
                print("Opcion no valida")
        except ValueError:
            print("Porfavor introduzca un valor numerico")




