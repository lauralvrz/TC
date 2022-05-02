import numpy as np
from cv2 import cv2
import sys
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from PIL import Image as im

def imagen_a_array(img):
    """
    Esta funcion coge una imagen RGB cualguiera y la pasa a un array de 0s y 1s,
    siendo el tamanyo de palabra 8 bits
    """

    imagen_array = []

    #La paso a array
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            for z in range(3): #RGB

                # Cogemos el valor RGB
                palabra = img[x][y][z]
                # Pasamos a binario de tamanyo fijo 8
                palabra = ( bin(palabra)[2:] ).zfill(8)
                # Pasamos a lista
                lst = [int(i) for i in str(palabra)]
                # Anyadimos al array final
                imagen_array.extend(lst)

    return imagen_array


# funcion que pase un vector a F2.
def a_base_2(v):
    for i in range(len(v)):
        v[i] = v[i] % 2
        
        
def comprimir_palabra(v, H, k):
    print("Comprimiendo palabra")

    """Esta funcion calcula el sindrome de v, decodifica la palabra usando el sindrome
    y devuelve los primeros k bits."""

    sindrome = np.dot(H,v)
    a_base_2(sindrome)
    ret = v

    # Buscamos a que columna corresponde el sindrome y descodificamos
    for ncol in range(len(H[0:])):

        columna = H[:ncol]
        x = ""
        for i in columna:
            x += str(i)
        
        if x == str(sindrome):
            ret[ncol] = (ret[ncol] + 1) % 2
        
        break

    return ret[:k]


def comprimir_imagen(src, H, n, k):
    print("Comprimiendo imagen")
    
    """ Esta funcion recibe la ruta de una imagen y los datos del codigo
    y devuelve la imagen comprimida."""

    img = cv2.imread(src)
    array = imagen_a_array(img)
    imagen_comprimida = []

    # Parte entera
    palabras_completas = int(len(array)/n)

    # Comprimimos las palabras
    for i in range(palabras_completas-1):

        palabra_comprimida = comprimir_palabra(array[i * n : i * n + n], H, k)
        imagen_comprimida.extend(palabra_comprimida)

    # Anyadimos el final de la imagen, los bits que sobran
    if ((len(array)/float(n)) % 1 != 0):
        start = (palabras_completas-1) * n + n
        imagen_comprimida.extend(array[(palabras_completas-1)*n:])
        
    # Imagen comprimida
    print(imagen_comprimida)
    
    
    # Debemos ademas guardar el shape para poder descomprimirla
    imagen_ret = { "array": imagen_comprimida, "shape": img.shape,
        "u_size": sys.getsizeof(array), "c_size": sys.getsizeof(imagen_comprimida) }

    return imagen_ret
    
    
def descomprimir_imagen(img_c, G, k):
    print("Descomprimiendo imagen")

    img = []
    ret = []

    palabras_completas = int(len(img_c['array'])/k)

    # Decodificamos las palabras
    for i in range(palabras_completas-1):
        palabra = img_c['array'][i * k : i * k + k]
        original = np.dot(palabra, G)
        a_base_2(original)
        img.extend(original)

    # Anyadimos el final de la imagen
    if ((len(img_c['array'])/float(k)) % 1 != 0.):
        start = (palabras_completas-1) * k + k
        img.extend(img_c['array'][start:])

    # Pasamos de binario a decimal
    for i in range(int(len(img)/8)):
        num = img[i * 8 : i * 8 + 8]
        ret.append(255 - int(''.join(map(str,num)),2))

    # Anyadimos los bits que faltan debido a errores de redondeo

    while( len(ret) != (img_c['shape'][0] * img_c['shape'][1] * img_c['shape'][2])):
        ret.append(0)

    img = np.array(ret).reshape(img_c['shape'])
    
    plt.imshow(img, interpolation='nearest')
    plt.show()

    return img


H = [[0,0,0,1,1,1,1],
     [0,1,1,0,0,1,1],
     [1,0,1,0,1,0,1]]

G = [[1,0,0,0,0,1,1],
     [0,1,0,0,1,0,1],
     [0,0,1,0,1,1,0],
     [0,0,0,1,1,1,1]]


print("Comprimir y descomprimir imagenes usando Hamming(3,2):")
comprimida = comprimir_imagen("Kanagawa.jpg", H, 7, 4)
img4 = descomprimir_imagen(comprimida, G, 4)
print("Tamanyo comprimida: ", comprimida['c_size'], " Tamanyo descomprimida: ",\
    comprimida['u_size'], " Ratio: ",\
        float(comprimida['c_size'])/float(comprimida['u_size']))
