import cv2
import numpy


#Usaremos as imagens fornecidas pelo professor para realizar os testes


input_img = cv2.imread("C:\\Users\\danil\\Desktop\\python\\trab_tpi\\input_img\\img15.jpg")
print(input_img)

#Primeiro passo: redimensionar o tamanho das imagens de entrada.
ESCALA = 30
largura = int(input_img.shape[1] * ESCALA / 100)
altura = int(input_img.shape[0] * ESCALA / 100)
dim = (largura, altura)
img_redim = cv2.resize(input_img, dim, interpolation = cv2.INTER_AREA)

#Aplicando filtro Gaussiano
blur = cv2.GaussianBlur(img_redim, (5,5), 0)

#Convertendo para grayscale
grayscale = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)



cv2.imshow("img", blur)
cv2.waitKey(0)


