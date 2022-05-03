#!/usr/bin/env python3

import random

wordlength = 12

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

B = [[0,1,1,1,1,1,1,1,1,1,1,1],
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
    result = ''
    for bit in bitstring:
        if random.uniform(0,1) <= p:
            if bit == '0':
                bit = '1'
            else:
                bit = '0'
        result += bit
    return result


# Multiplicar dos matrices sobre el campo de Galois GF2
def GF2_matrix(A,B):
    C_rows = len(A)
    C_cols = len(B[0])
    C = [[0 for k in range(C_cols)] for i in range(C_rows)]

    for i in range(C_rows):
        for k in range(C_cols):
            for j in range(len(A[0])):
                C[i][k] ^= (A[i][j] & B[j][k])
    return C


# Dada la matriz (n x i) A y la matriz (n x j) B,
# devuelve la matriz (n x (i + j)) (A|B)
def conjoin(A,B):
    columns = len(A[0]) + len(B[0])
    rows = len(A)
    conjoined = [0] * rows
    for row in range(rows):
        conjoined[row] = A[row] + B[row]
    return conjoined


# Devuelve la traspuesta de la matriz
def transpose(matrix):
    t_rows = len(matrix[0])
    t_cols = len(matrix)
    transposed = [[0 for k in range(t_cols)] for i in range(t_rows)]

    for i in range(t_rows):
        for j in range(t_cols):
            transposed[i][j] = matrix[j][i]
    return transposed


# Devuelve la columna n de la matriz
def get_column(matrix, col_num):
    B_col = [[0] * len(matrix[0])]
    for k in range(len(B[0])):
        B_col[0][k] = B[col_num][k]
    return B_col


# Añadir dos vectores sobre el campo de Galois GF2
def add_vectors(A,B):
    length = len(A[0])
    C = [[0]*length]
    for index in range(length):
        C[0][index] = A[0][index] ^ B[0][index]
    return C


# Unir los elementos de un vector y devolver una cadena de bits
def string_from_vector(vector):
    return ''.join([str(j) for j in vector[0]])


# Devuelve el nombre del archivo como una cadena de bits
# def get_bitstream(filename):
#     with open(filename, 'rb') as fh:
#         bytestream = fh.read()
#         bitstream = ''
#         for byte in bytestream:
#         #     ascii = ord(char)
#             binary = '{0:08b}'.format(byte)
#             bitstream += binary
#     return bitstream

def get_bitstream(cadena):
    # cadenaB = cadena.encode("utf-8")
    bitstream = ''
    # for byte in cadena:
    binary = '{0:08b}'.format(cadena)
    bitstream += binary
    # print(bitstream)
    return bitstream


# Rellenar el flujo de bits con 1s para que el número de bits sea múltiplo de la longitud de la palabra
# Añade el prefijo que indica el número de 1s añadidos
def padder(bitstream, wordlength=12):
    prefix, padding = '',''
    length = len(bitstream)
    remainder = length % wordlength
    if remainder != 0:
        padlength = wordlength - remainder
        prefix = '{0:012b}'.format(padlength)
        padding = '1' * padlength
    return prefix + bitstream + padding


# Eliminar el prefijo y los bits de relleno
def unpadder(bitstream, wordlength=12):
    padlength = int(bitstream[:wordlength],2)
    return bitstream[wordlength:-padlength]


# Convertir una cadena de bits en un vector GF2
def get_vector(word):
    vector = [[]]
    for char in word:
        vector[0].append(int(char))
    return vector


# Obtener la matriz generadora del código Golay binario extendido (G24)
G = conjoin(I,B)


# Obtener la transposición de la matriz de comprobación de paridad para G24
Ht = transpose(conjoin(B,I))


print('''--- Codificando ---''')

# archivo = open("texto.txt", "r")
#texto = archivo.read()

with open("texto.txt", 'rb') as fh:
    texto = fh.read()

msgerror = ''
msgcorregido = ''

for palabra in texto:
    bitstream = get_bitstream(palabra)

    # bitstream = get_bitstream('texto.txt')
    # bitstream = get_bitstream('flower.png')
    padstream = padder(bitstream)

    # Inicializar la cadena para los datos codificados
    encoded = ''

    # Dividir los datos en palabras de 12 bits, codificar cada palabra
    # utilizando el código binario extendido de Golay y convertirlo en cadena
    for index in range(0,len(padstream),wordlength):
        word = padstream[index:index+wordlength]
        vector = get_vector(word)
        Golay_vector = GF2_matrix(vector,G)
        Golay_word = string_from_vector(Golay_vector)
        encoded += Golay_word

    bitstream_len = len(bitstream)
    encoded_len = len(encoded)


    errbits = ''
    outbits = ''

    # Obtener segmentos de 24 bits del flujo de bits codificado y aleatorizarlos
    for index in range(0,encoded_len,24):
        word = encoded[index:index+24]
        orig = word
        word = randomize(word)
        errbits += word # Añade los bits aleatorios a errbits (msg recibido)

        # Transformar una palabra de 24 bits en un vector y calcular el síndrome
        wordvector = get_vector(word)
        syndrome1 = GF2_matrix(wordvector,Ht)
        weight = sum(syndrome1[0]) # Peso del síndrome


        # Caso 1: si el peso Hamming del síndrome es <= 3, conocemos el vector de error
        if weight <= 3:
            error_L = [0] * 12
            error = [error_L + syndrome1[0]]

        # Caso 2: Si no es así (w>3), lo procesamos más...
        else:
            S1_dict = {}
            small_weights = {}
            for j in range(12):
                sum_vec = add_vectors(syndrome1,get_column(B,j)) #S1 + Bi
                syn_weight = sum(sum_vec[0]) #w(S1 + Bi)
                wt = (syn_weight, sum_vec)
                if syn_weight <= 2:
                    small_weights[j] = wt

            # Caso 2.1: peso de un subvector <= 2
            if len(small_weights) == 1:
                error = [I[list(small_weights.keys())[0]] + sum_vec[0]]

            # Caso 2.2: varios pesos de subvectores <= 2
            elif len(small_weights) > 1:
                weightlist = [small_weights[key][0] for key in small_weights]
                smallest = min(weightlist)
                for key in small_weights:
                    if small_weights[key][0] == smallest:
                        error = small_weights[key][1]
                        break

            # Caso 2.3: todos los pesos de los subvectores > 3
            else:
                # Calcular el síndrome2
                syndrome2 = GF2_matrix(syndrome1, transpose(B))
                weight2 = sum(syndrome2[0])

                # Caso 2.3.1: Si el peso del síndrome2 <= 3, conocemos el error
                if weight2 <= 3:
                    error_R = [0] * 12
                    error = [syndrome2[0] + error_R]

                # Caso 2.3.2: En caso contrario, procesamos más...
                else:
                    small_weights = {}
                    for j in range(12):
                        wt = ()
                        sum_vec = add_vectors(syndrome2, get_column(B, j))
                        syn_weight = sum(sum_vec[0])
                        wt = (syn_weight, sum_vec)
                        if syn_weight <= 2:
                            error = [sum_vec[0] + I[j]]
                            break
                        else:
                            error = [[0] * 24]


        if not error:
            error = [[0] * 24]
        # Palabra de Golay corregida = (vector recibido) - (vector de error)
        corrected = add_vectors(wordvector,error)
        corr_str = string_from_vector(corrected)
        # Texto transmitido = primera mitad de la palabra Golay corregida
        outbits += corr_str[:12]


    # Obtener los bits del mensaje recibido no corregido (para comparar con el mensaje corregido)
    errbits_out = ''
    for j in range(0,len(errbits),24):
        errbits_out += errbits[j:j+12]

    mssg = ''
    errmssg = ''

    # Eliminar el relleno
    outbits = outbits[12:]
    errbits_out = errbits_out[12:]

    # Convertir los bits del mensaje corregido en una cadena
    
    for i in range(0,len(outbits),8):
        charbits = outbits[i:i+8]
        outchar = chr(int(charbits,2))
        # mssg += outchar.to_bytes((outchar.bit_length() + 7) // 8, 'big').decode()
        mssg += outchar

    # Convertir los bits de los mensajes no corregidos en una cadena
    for i in range(0,len(errbits_out),8):
        charbits = errbits_out[i:i+8]
        outchar = chr(int(charbits,2))
        errmssg += outchar
        
    #print(mssg)
        
    msgerror += errmssg
    msgcorregido += mssg
    
# Salida
print("\n Mensaje con errores:")
print(msgerror)
print("\n Mensaje corregido:")
print(msgcorregido)
print("\n")