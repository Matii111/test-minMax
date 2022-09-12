import funciones
import globales
import librerias





# main
#el main es simple solo le pide al jugador que escriba
#la palabra "comenzar" para ejecutar el juego


comenzar = ""


while comenzar != "COMENZAR":

    comenzar = input("Escriba comenzar para ejecutar el juego: \n").upper() # read just one linea

if comenzar == "COMENZAR":

    print("\n")

    funciones.REVERSI()


