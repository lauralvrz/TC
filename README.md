---
title: "Código de Golay binario G24"
author: "Laura Álvarez Iglesias"
date: "10 Mayo 2022"
output: pdf_document
---

<span style="font-family: Noto Serif">

## Código de Golay binario _G<sub>24</sub>_

Teoría de Códigos, Laura Álvarez Iglesias

---

### 1. Introducción

El código de Golay binario _G<sub>24</sub>_ es un código (corrector de errores triples) sobre _Z<sub>2</sub>_ cuyos parámetros son _(24, 12, 8)_, su matriz generadora es de la forma _G = (I<sub>12</sub> A)_ siendo _I<sub>12</sub>_ la matriz identidad de orden 12 y _A_ la matriz cuadrada 12x12

$$A=\begin{pmatrix}
0&1&1&1&1&1&1&1&1&1&1&1\\
1&1&1&0&1&1&1&0&0&0&1&0\\
1&1&0&1&1&1&0&0&0&1&0&1\\
1&0&1&1&1&0&0&0&1&0&1&1\\
1&1&1&1&0&0&0&1&0&1&1&0\\
1&1&1&0&0&0&1&0&1&1&0&1\\
1&1&0&0&0&1&0&1&1&0&1&1\\
1&0&0&0&1&0&1&1&0&1&1&1\\
1&0&0&1&0&1&1&0&1&1&1&0\\
1&0&1&0&1&1&0&1&1&1&0&0\\
1&1&0&1&1&0&1&1&1&0&0&0\\
1&0&1&1&0&1&1&1&0&0&0&1\\
\end{pmatrix}.$$

El objetivo de esta práctica es implementar el código de Golay binario _G<sub>24</sub>_ para la detección y corrección de errores en la transmisión de texto por un canal con ruido. El lenguaje de programación que se ha utilizado para la implementación es Python 3.
<br>

### 2. Funcionamiento

Primero se lee el archivo de texto para poder iniciar la transmisión. Las palabras del texto se pasan a binario, se dividen en palabras de 12 bits y se codifican utilizando el código binario de Golay. Luego se obtienen segmentos de 24 bits del conjunto de palabras codificadas y se aleatorizan para simular el canal con ruido.
Para cada uno de estos segmentos de 24 bits se aplica el siguiente algoritmo:

_**Algortimo:**_ Recibida una palabra binaria _**r**_ de longitud 24,
(i) Se calcula el síndrome de la palabra recibida, _**s**_ = _**r**_ _G<sup> tr</sup>_.