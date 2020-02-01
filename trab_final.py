import cv2
import numpy as np


def rec_coin(img):
    # Reduzindo a imagem para 30% do seu tamanho original
    img_resized = cv2.resize(img, (0, 0), fx=0.3, fy=0.3)
    # Convertendo para grayscale
    gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    # Aplicando Filtro Gaussiano
    img_blur = cv2.GaussianBlur(gray, (7, 7), 0)  # resultado melhor com GaussianBlur
    # Binarização com limiar adaptativo e Gaussiano
    th2 = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 17,
                                3)  # 17,3 RECONHECE MOEDA SUPERIOR

    ##RECONHECIMENTO E DESENHO DAS CINCUNFERÊNCIAS ENCONTRADAS##

    # Reconhecimento dos círculos com HoughCircles. Parâmetros arbitrários
    circles = cv2.HoughCircles(img_blur, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=50, minRadius=20, maxRadius=65)

    # Desenhando a circunferência e centro dos círculos encontrados e contagem de moedas
    count_moedas = 0
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # Draw outer circle
            count_moedas += 1
            cv2.circle(img_resized, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # Draw inner circle
            cv2.circle(img_resized, (i[0], i[1]), 2, (0, 0, 255), 3)

    return count_moedas


def rec_note(img):
    # Reduzindo a imagem para 20% do seu tamanho original
    img_resized = cv2.resize(img, (0, 0), fx=0.2, fy=0.2)

    # Convertendo para grayscale
    gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    # Aplicando Filtro Gaussiano
    img_blur = cv2.GaussianBlur(gray, (9, 9), 0)  # resultado melhor com GaussianBlur

    th2 = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 23, 3)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    #eroded = cv2.erode(th2, kernel, iterations = 2)

    # testes
    edged = cv2.Canny(th2, 4, 150)
    # edged = cv2.Canny(img_resized, 4, 150)
    #cv2.imshow("Edges", edged)

    
    closed = cv2.morphologyEx(edged, cv2.MORPH_OPEN, kernel)

    cv2.imshow("Closed", closed)
    cv2.waitKey(0)

    (cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    count_notes = 0

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        cv2.drawContours(img_resized, [approx], -1, (0, 255, 0), 2)
        x, y, w, h = cv2.boundingRect(c)
        if w > 150 and h > 160:
            count_notes = count_notes + 1
    cv2.imshow("Closed", img_resized)
    cv2.waitKey(0)
    return count_notes


img = cv2.imread("C:\\Users\\danil\\Desktop\\python\\trab_tpi\\input_img\\0c2n.jpg", cv2.IMREAD_COLOR)

count_coin = rec_coin(img)
count_note = rec_note(img)
print("%dc%dn.jpg" % (count_coin, count_note))