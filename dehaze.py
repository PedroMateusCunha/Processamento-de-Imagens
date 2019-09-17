# -*- coding: utf-8 -*-
import cv2
import numpy as np
import argparse
from matplotlib import pyplot as plt


print("""\n
8888888b.           888                                 
888  "Y88b          888                                 
888    888          888                                 
888    888  .d88b.  88888b.   8888b.  88888888  .d88b.  
888    888 d8P  Y8b 888 "88b     "88b    d88P  d8P  Y8b 
888    888 88888888 888  888 .d888888   d88P   88888888 
888  .d88P Y8b.     888  888 888  888  d88P    Y8b.     
8888888P"   "Y8888  888  888 "Y888888 88888888  "Y8888                                                  
\n""")

#Função do canal escuro
def dark_channel(img, tamanho = 15):
    r,g,b = cv2.split(img)#separar a imagem
    min_img = cv2.min(r, cv2.min(g, b))#menor vetor
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (tamanho, tamanho))#gera estrutura retangular
    dc_img = cv2.erode(min_img,kernel)#Corrige imagem
    return dc_img

#funcao de atmosfera
def get_atmo(img, percent = 0.001):
    mean_perpix = np.mean(img, axis = 2).reshape(-1)#da forma a matriz sem alterar os dados
    mean_topper = mean_perpix[:int(img.shape[0] * img.shape[1] * percent)]
    return np.mean(mean_topper)#media dos vetores

#funcao de translucidez
def get_trans(img, atom, w = 0.95):
    x = img / atom
    t = 1 - w * dark_channel(x, 15)
    return t

#Funcao de Filtro Guiado
def guided_filter(p, i, r, e):
    """
    :parametros p: input imagem
    :parametros i: guidance imagem
    :parametros r: radius
    :parametros e: regularization
    :return: filtering output q
    """
    #1
    mean_I = cv2.boxFilter(i, cv2.CV_64F, (r, r))#desfoca imagem | filtro gradiente de imagem
    mean_p = cv2.boxFilter(p, cv2.CV_64F, (r, r))
    corr_I = cv2.boxFilter(i * i, cv2.CV_64F, (r, r))
    corr_Ip = cv2.boxFilter(i * p, cv2.CV_64F, (r, r))
    #2
    var_I = corr_I - mean_I * mean_I
    cov_Ip = corr_Ip - mean_I * mean_p
    #3
    a = cov_Ip / (var_I + e)
    b = mean_p - a * mean_I
    #4
    mean_a = cv2.boxFilter(a, cv2.CV_64F, (r, r))
    mean_b = cv2.boxFilter(b, cv2.CV_64F, (r, r))
    #5
    q = mean_a * i + mean_b
    return q

#Funcao Principal para extração da Neblina
def dehaze(path, output = None):
    im = cv2.imread(path)
    img = im.astype('float64') / 255
    img_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype('float64') / 255#cinza escala

    atom = get_atmo(img)
    trans = get_trans(img, atom)
    trans_guided = guided_filter(trans, img_gray, 20, 0.0001)
    trans_guided = cv2.max(trans_guided, 0.25)

    result = np.empty_like(img)#retorna uma copia da matriz
    for i in range(3):
        result[:,:,i] = (img[:, :, i] - atom) / trans_guided + atom

    #Inversão de Cores pro Matplotlib
    b,g,r = cv2.split(img)
    img2 = cv2.merge([r,g,b])
    b,g,r = cv2.split(result)
    result2 = cv2.merge([r,g,b])

    #Plotando as imagens
    plt.subplot(121),plt.imshow(img2),plt.title('Imagem Original')
    plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(result2),plt.title('Imagem Sem Neblina')
    plt.xticks([]), plt.yticks([])
    plt.show()
    print("\n")
    cv2.waitKey()
    cv2.destroyAllWindows()
    #cv2.imshow("source",img)
    #cv2.imshow("result", result)
    #cv2.waitKey()
    if output is not None:
        cv2.imwrite(output, result * 255)

#sistema de argumentos 
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input')
parser.add_argument('-o', '--output')
args = parser.parse_args()

#modulação de codigo
if __name__ == '__main__':
    if args.input is None:
        print("*"+"-"*116+"*")
        print("|Utilize: python dehaze.py -i <nome_do_arquivo>.<extencao_arquivo> -o <nome_arquivo_modificado>.<extencao_do_arquivo>|")
        print("*"+"-"*116+"*")
        print("Ex: python dehaze.py -i teste1.png -o teste2.png")
        print("[!] O arquivo deve estar no mesmo diretorio do programa!")
    else:
	    dehaze(args.input, args.output)
