import sys
import cv2
from matplotlib import pyplot as plt

#Funcao de ajuda ao user
def ajuda():
	print("""\n
    dD d8b   db  .d88b.  Cb     d888888b .d8888. d88888b 
  d8'  888o  88 .8P  Y8.  `8b     `88'   88'  YP 88'     
 d8    88V8o 88 88    88    8b     88    `8bo.   88ooooo 
C88    88 V8o88 88    88    88D    88      `Y8b. 88~~~~~ 
 V8    88  V888 `8b  d8'    8P    .88.   db   8D 88.     
  V8.  VP   V8P  `Y88P'   .8P   Y888888P `8888Y' Y88888P 
    VD                   CP                              
                                                         
\n""")
	print("*"+"-"*64+"*")
	print("|Utilize: python noise.py <nome_do_arquivo>.<extencao_do_arquivo>|")
	print("*"+"-"*64+"*")
	print("Ex: python noise.py teste.jpg")
	print("[!] O arquivo deve estar no mesmo diretorio do programa!")


#Exemplificar uso do Programa
if len(sys.argv) != 2:
    ajuda()
    sys.exit(1)
elif sys.argv[1] == 'help':
	ajuda()
	sys.exit(1)

def creditos():
	print("""\n
 █    ██ ▓█████   ██████  ██▓███   ██▓
 ██  ▓██▒▓█   ▀ ▒██    ▒ ▓██░  ██▒▓██▒
▓██  ▒██░▒███   ░ ▓██▄   ▓██░ ██▓▒▒██▒
▓▓█  ░██░▒▓█  ▄   ▒   ██▒▒██▄█▓▒ ▒░██░
▒▒█████▓ ░▒████▒▒██████▒▒▒██▒ ░  ░░██░
░▒▓▒ ▒ ▒ ░░ ▒░ ░▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░░▓  
░░▒░ ░ ░  ░ ░  ░░ ░▒  ░ ░░▒ ░      ▒ ░
 ░░░ ░ ░    ░   ░  ░  ░  ░░        ▒ ░
   ░        ░  ░      ░            ░  
                                      
""")
	print("")
	print("*"+"-"*64+"*")
	print("DEVELOPED BY:\nPEDRO CUNHA\nSEGUNDO PASSOS\nFABRICIO SWAGGER\nMARCELO SEGUNDO")
	print("*"+"-"*64+"*")

#Funcao de extracao
def extrair():
	#tentativas e erros
	try:
	
		#recebe a leiturar da imagem passada no argumento
		imagem = cv2.imread(sys.argv[1])

		#aplica o filtro de mediana da biblioteca OpenCV na variavel mediana
		#utilizando uma mascara 5x5﻿
		filtro = cv2.medianBlur(imagem, 5)

		#subplot cria os eixos na posicao da grade especificada subplot ( nrows , ncols , index )
		#imshow exibe a imagem
		#title coloca um titulo na comparacao
		#xticks define o local e rotulo do eixo x
		#yticks define o local e rotulo do eixo y
		#show exibe a figura completa
		plt.subplot(121),plt.imshow(imagem),plt.title('Imagem Original')
		plt.xticks([]), plt.yticks([])
		plt.subplot(122),plt.imshow(filtro),plt.title('Imagem Mediana')
		plt.xticks([]), plt.yticks([])
		#plt.show()
		#histograma = plt.hist(imagem.ravel(), 256, [0, 256])
		plt.show()
		print("\n")
		cv2.waitKey()
		cv2.destroyAllWindows()

		#Laço de repetição para salvar a imagem processada
		while True:
			resp = input("Deseja salvar a imagem modificada? (y/n)").lower()
			if resp == 'y':
				#salva a imagem
				#nome = input("[*] Insira o nome do Arquivo: ") 
				cv2.imwrite("mediana.jpeg", filtro)
				break
			elif resp == 'n':
				break
			else:
				print("[*] Insira uma opcao valida\n")
		creditos()
	except TypeError:
		print("\n[*] NOME DE IMAGEM INCORRETO!")
		print("[*] TENTE NOVAMENTE COM NOME E EXTENCAO CORRETOS!!!")
		print("[*] O ARQUIVO DEVE ESTAR NO MESMO DIRETORIO QUE O PROGRAMA")
	except Exception as erro: #erros a parte
		print("[*] {}".format(erro))

extrair()