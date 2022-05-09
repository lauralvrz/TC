#!/usr/bin/env python3

import random

longitud = 12

I = [[1,0,0,0,0,0,0,0,0,0,0,0],
     [0,1,0,0,0,0,0,0,0,0,0,0],
     [0,0,1,0,0,0,0,0,0,0,0,0],
     [0,0,0,1,0,0,0,0,0,0,0,0],
     [0,0,0,0,1,0,0,0,0,0,0,0],
     [0,0,0,0,0,1,0,0,0,0,0,0],
     [0,0,0,0,0,0,1,0,0,0,0,0],
     [0,0,0,0,0,0,0,1,0,0,0,0],
     [0,0,0,0,0,0,0,0,1,0,0,0],
     [0,0,0,0,0,0,0,0,0,1,0,0],
     [0,0,0,0,0,0,0,0,0,0,1,0],
     [0,0,0,0,0,0,0,0,0,0,0,1]]

A = [[0,1,1,1,1,1,1,1,1,1,1,1],
     [1,1,1,0,1,1,1,0,0,0,1,0],
     [1,1,0,1,1,1,0,0,0,1,0,1],
     [1,0,1,1,1,0,0,0,1,0,1,1],
     [1,1,1,1,0,0,0,1,0,1,1,0],
     [1,1,1,0,0,0,1,0,1,1,0,1],
     [1,1,0,0,0,1,0,1,1,0,1,1],
     [1,0,0,0,1,0,1,1,0,1,1,1],
     [1,0,0,1,0,1,1,0,1,1,1,0],
     [1,0,1,0,1,1,0,1,1,1,0,0],
     [1,1,0,1,1,0,1,1,1,0,0,0],
     [1,0,1,1,0,1,1,1,0,0,0,1]]


# Función de aleatorización para simular la transmisión por un canal ruidoso
def randomize(bitstring, p=0.02):
    resultado = ''
    for bit in bitstring:
        if random.uniform(0,1) <= p:
            if bit == '0':
                bit = '1'
            else:
                bit = '0'
        resultado += bit
    return resultado


# Multiplicar dos matrices
def multiplicar_matrices(X,Y):
    num_filas = len(X)
    num_columnas = len(Y[0])
    Z = [[0 for k in range(num_columnas)] for i in range(num_filas)]

    for i in range(num_filas):
        for k in range(num_columnas):
            for j in range(len(X[0])):
                Z[i][k] ^= (X[i][j] & Y[j][k])
    return Z


# Dada la matriz (n x i) X y la matriz (n x j) Y,
# devuelve la matriz (n x (i + j)) (X|Y)
def concatenar(X,Y):
    num_filas = len(X)
    resultado = [0] * num_filas
    for fila in range(num_filas):
        resultado[fila] = X[fila] + Y[fila]
    return resultado


# Devuelve la traspuesta de la matriz
def traspuesta(matriz):
    t_filas = len(matriz[0])
    t_cols = len(matriz)
    resultado = [[0 for k in range(t_cols)] for i in range(t_filas)]

    for i in range(t_filas):
        for j in range(t_cols):
            resultado[i][j] = matriz[j][i]
    return resultado


# Devuelve la fila número "n" de la matriz dada
def get_fila(matriz, n):
    fila_n = [[0] * len(matriz[0])]
    for k in range(len(matriz[0])):
        fila_n[0][k] = matriz[n][k]
    return fila_n


# Sumar dos vectores
def sumar_vectores(X,Y):
    longitud = len(X[0])
    Z = [[0]*longitud]
    for index in range(longitud):
        Z[0][index] = X[0][index] ^ Y[0][index]
    return Z


# Unir los elementos de un vector y devolver una cadena de bits
def vector_a_string(vector):
    return ''.join([str(j) for j in vector[0]])


# Convierte la cadena (parametro) a una cadena de bits
def get_bits(cadena):
    bitstream = ''
    # for byte in cadena:
    binary = '{0:08b}'.format(cadena)
    bitstream += binary
    # print(bitstream)
    return bitstream


# Rellenar el flujo de bits con 1s para que el número de bits sea múltiplo de la longitud de la palabra
# Añade el prefijo que indica el número de 1s añadidos
def rellenar(bitstream, longitud=12):
    prefijo, padding = '',''
    length = len(bitstream)
    resto = length % longitud
    if resto != 0:
        padlength = longitud - resto
        prefijo = '{0:012b}'.format(padlength)
        padding = '1' * padlength
    return prefijo + bitstream + padding


# Convertir una cadena de bits en un vector
def get_vector(word):
    vector = [[]]
    for char in word:
        vector[0].append(int(char))
    return vector


# Obtener la matriz generadora del código Golay binario (G24)
G = concatenar(I,A)


# Obtener la transposición de la matriz de comprobación de paridad para G24
traspuestaG = traspuesta(concatenar(A,I))


print("\n--- Codificando ---")

# archivo = open("texto.txt", "r")
#texto = archivo.read()

# Leemos el archivo
with open("texto.txt", 'rb') as fh:
    texto = fh.read()

msj_errores = ''
msj_corregido = ''

for palabra in texto:
    # Convertimos la palabra a binario
    bitstream = get_bits(palabra)
    datos = rellenar(bitstream)

    # Inicializar la cadena para los datos codificados
    encoded = ''

    # Dividir los datos en palabras de 12 bits, codificar cada palabra
    # utilizando el código binario de Golay y convertirlo en cadena
    for index in range(0,len(datos),longitud):
        palabra_12 = datos[index:index+longitud]
        vector = get_vector(palabra_12)
        Golay_vector = multiplicar_matrices(vector,G)
        Golay_palabra = vector_a_string(Golay_vector)
        encoded += Golay_palabra

    palabra_error = '' # Inicializamos la palabra con errores
    palabra_corregida = '' # Inicializamos la palabra corregida

    # Obtener segmentos de 24 bits del flujo de bits codificado y aleatorizarlos
    for index in range(0,len(encoded),24):
        palabra_24 = encoded[index:index+24]
        palabra_24 = randomize(palabra_24)
        palabra_error += palabra_24 # Añade los bits aleatorios a palabra_error (msg recibido)

        # Transformar una palabra de 24 bits en un vector y calcular el síndrome
        vector_24 = get_vector(palabra_24)
        sindrome1 = multiplicar_matrices(vector_24,traspuestaG)
        peso = sum(sindrome1[0]) # Peso del síndrome (número de unos)


        # Caso 1: si el peso Hamming del síndrome es <= 3, conocemos el vector de error
        if peso <= 3:
            error_L = [0] * 12
            error = [error_L + sindrome1[0]]

        # Caso 2: Si no es así (w>3), lo procesamos más...
        # Calculamos el peso w(s + Ai) para las filas de A
        else:
            peso_menor = {}
            for j in range(12):
                sum_vec = sumar_vectores(sindrome1,get_fila(A,j)) # s + Ai
                peso_fila = sum(sum_vec[0]) # w(s + Ai)
                wt = (peso_fila, sum_vec) # (peso, sindrome + fila i)
                if peso_fila <= 2: 
                    peso_menor[j] = wt

            # Caso 2.1: peso <= 2 para alguna fila
            if len(peso_menor) == 1:
                # Obtenemos la fila i de A
                fila = list(peso_menor.keys())[0]
                # ui = palabra de longitud 12 con un 1 en la i-ésima componente
                # y 0's en las restantes
                ui = I[fila]
                # error = (ui + (sindrome + fila))
                error = [ui + sum_vec[0]]

            # Caso 3: todos los pesos son > 3
            else:
                # Calcular el síndrome2
                sindrome2 = multiplicar_matrices(sindrome1, A)
                peso2 = sum(sindrome2[0])

                # Caso 3.1: Si el peso del síndrome2 <= 3, conocemos el error
                if peso2 <= 3:
                    error_fila = [0] * 12
                    error = [sindrome2[0] + error_fila]

                # Caso 3.2: En caso contrario, procesamos más...
                # Calculamos el peso w(sindrome2 + Ai) para las filas de A
                else:
                    for j in range(12):
                        wt = ()
                        sum_vec = sumar_vectores(sindrome2, get_fila(A, j))
                        peso_fila = sum(sum_vec[0])
                        wt = (peso_fila, sum_vec)
                        if peso_fila <= 2:
                            error = [sum_vec[0] + I[j]]
                            break
                        else:
                            error = [[0] * 24]

        # Si no se detecta error
        if not error:
            error = [[0] * 24]
        
        # Palabra de Golay corregida = (vector recibido) - (vector de error)
        corregida = sumar_vectores(vector_24,error)
        corregida_str = vector_a_string(corregida)
        
        # Palabra transmitida (binario) = primera mitad de la palabra Golay corregida
        palabra_corregida += corregida_str[:12]

    # Obtener los bits del mensaje recibido no corregido
    # (dividir la palabra_error cada 12 bits)
    bits_error = ''
    for j in range(0,len(palabra_error),24):
        bits_error += palabra_error[j:j+12]

    # Eliminar el relleno
    palabra_corregida = palabra_corregida[12:]
    bits_error = bits_error[12:]

    # Convertir los bits del mensaje corregido en una cadena
    for i in range(0,len(palabra_corregida),8):
        charbits = palabra_corregida[i:i+8]
        outchar = chr(int(charbits,2))
        msj_corregido += outchar

    # Convertir los bits de los mensajes no corregidos en una cadena
    for i in range(0,len(bits_error),8):
        charbits = bits_error[i:i+8]
        outchar = chr(int(charbits,2))
        msj_errores += outchar


# Para poder mostrar colores por pantalla
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'    


# Salida
print(color.RED +"\n Mensaje con errores:" + color.END)
print(msj_errores)
print(color.GREEN + "\n Mensaje corregido:" + color.END)
print(msj_corregido)
print("\n")