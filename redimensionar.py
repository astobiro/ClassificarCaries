import cv2
import glob
import timeit
import numpy as np
import random

def preencher(image):
	#Preenche uma imagem de fundo com a imagem do parametro
	temp = np.zeros((28, 28), np.uint8)
	width = image.shape[0]
	height = image.shape[1]
	for i in range(width):
		for j in range(height):
			temp[i][j] = image[i][j]

	return temp

def resize(image):
	# Redimensiona uma imagem para uma escala 28x28 proporcionalmente e as coloca em uma imagem 28x28 de fundo
	x = image.shape[0]
	y = image.shape[1]
	if x <= 28 and y <= 28:
		tempImg = image
		resimage = preencher(tempImg)
	elif x > y:
		prevx = x
		x = 28
		y = int((y*28)/prevx)
		tempImg = cv2.resize(image, (x, y))
		resimage = preencher(tempImg)
	elif y > x:
		x = int((x*28)/y)
		y = 28
		tempImg = cv2.resize(image, (x, y))
		resimage = preencher(tempImg)
	elif x == y:
		x = 28
		y = 28
		tempImg = cv2.resize(image, (x, y))
		resimage = preencher(tempImg)
	else:
		resimage = None

	return resimage

def resizeAll(les, nonles):
	# Redimensiona todas as imagens para uma escala 28x28
	resles = []
	resnonles = []
	for i in range(len(les)):
		tempImg = resize(les[i])
		resles.append(tempImg)

	for i in range(len(nonles)):
		tempImg = resize(nonles[i])
		resnonles.append(tempImg)

	return resles, resnonles

def checkInList(vet, el):
	#checa se um elemento está na lista
	for i in range(len(vet)):
		if el == vet[i]:
			return True
	return False

def removeElements(vet, els):
	#Concatena elementos não presentes nos indices da lista els em uma nova lista
	newlist = []
	for i in range(len(vet)):
		if checkInList(els, i):
			i += 1
		else:
			newlist.append(vet[i])

	return newlist

def saveImagesToFolder(images, folder, count):
	#salva cada imagem da lista no caminho especificado, com seu nome iniciando em count e incrementado
    counter = count
    print("Start saving:", counter)
    for i in range(len(images)):
        cv2.imwrite(folder + str(counter) + ".jpg", images[i])
        counter += 1
    print("End saving:", counter)
    return counter

def TreinoTeste(les, nonles):
	# Separa as imagens 100 lesões pra teste, 100 não lesões para teste e o resto para treino
	randles = []
	randnonles = []
	randomles = []
	randomnonles = []
	for i in range(100):
		newrandomles = random.randint(0, len(les)-1)
		if not checkInList(randomles, newrandomles):
			randomles.append(newrandomles)
		else:
			while checkInList(randomles, newrandomles):
				newrandomles = random.randrange(0, len(les)-1)
			randomles.append(newrandomles)

		newrandomnonles = random.randint(0, len(nonles)-1)
		if not checkInList(randomnonles, newrandomnonles):
			randomnonles.append(newrandomnonles)
		else:
			while checkInList(randomnonles, newrandomnonles):
				newrandomnonles = random.randrange(0, len(nonles)-1)
			randomnonles.append(newrandomnonles)

		randles.append(les[newrandomles])
		randnonles.append(nonles[newrandomnonles])

	treinoles = removeElements(les, randomles)
	treinononles = removeElements(nonles, randomnonles)

	return treinoles, randles, treinononles, randnonles

def rotate(image, angle):
	#rotaciona uma imagem em um determinado angulo
	x, y = image.shape
	M = cv2.getRotationMatrix2D((y/2, x/2), angle, 1)
	dst = cv2.warpAffine(image, M, (y, x))

	return dst

def generate9(image):
	# Gera 9 novas imagens para uma imagem, rotacionando e espelhando-a
	# rotacionada 90 graus
	img1 = rotate(image, 90)
	# rotacionada 90 graus e espelhada em x
	img2 = cv2.flip(img1, 0)
	# rotacionada 90 graus e espelhada em y
	img3 = cv2.flip(img1, 1)
	# rotacionada 180 graus
	img4 = rotate(image, 180)
	# rotacionada 180 graus e espelhada em x
	img5 = cv2.flip(img4, 0)
	# rotacionada 180 graus e espelhada em y
	img6 = cv2.flip(img4, 1)
	# rotacionada 270 graus
	img7 = rotate(image, 270)
	# rotacionada 270 graus e espelhada em x
	img8 = cv2.flip(img7, 0)
	# rotacionada 270 graus e espelhada em y
	img9 = cv2.flip(img7, 1)

	return img1, img2, img3, img4, img5, img6, img7, img8, img9

def rotateAndGenerateAll(trainles, trainnonles):
	# Gera 9 novas imagens para cada imagem de lesão e não lesão do treino
	newtrainles = []
	newtrainnonles = []
	for i in range(len(trainles)):
		temp = generate9(trainles[i])
		for j in range(len(temp)):
			newtrainles.append(temp[j])

	for i in range(len(trainnonles)):
		temp = generate9(trainnonles[i])
		for j in range(len(temp)):
			newtrainnonles.append(temp[j])

	return newtrainles, newtrainnonles

def main():
	print("Start")
	start = timeit.default_timer()
	#Carrega todas as imagens nas pastas em listas
	lImages = [cv2.imread(file, 0) for file in glob.glob("C:/Users/Artur/Dropbox/Projeto/Patches L/*.jpg")]
	nlImages = [cv2.imread(file, 0) for file in glob.glob("C:/Users/Artur/Dropbox/Projeto/Patches NL/*.jpg")]

	reslImages, resnlImages = resizeAll(lImages, nlImages)
	print("Redimensionados: ", len(reslImages), "lesões e", len(resnlImages), "não lesões")

	treinoles, testeles, treinononles, testenonles = TreinoTeste(reslImages, resnlImages)
	print(len(treinoles), len(testeles), len(treinononles), len(testenonles))

	newtrainles, newtrainnonles = rotateAndGenerateAll(treinoles, treinononles)
	print(len(newtrainles), len(newtrainnonles), len(newtrainles) + len(newtrainnonles) + 200)
	#Mistura os elementos das listas
	random.shuffle(newtrainles)
	random.shuffle(newtrainnonles)
	# c = s	aveImagesToFolder(newtrainles, "C:/Users/Artur/Desktop/Treino L/", 0)
	# c1 = saveImagesToFolder(testeles, "C:/Users/Artur/Desktop/Teste L/", c)
	# c2 = saveImagesToFolder(newtrainnonles, "C:/Users/Artur/Desktop/Treino NL/", c1)
	# c3 = saveImagesToFolder(testenonles, "C:/Users/Artur/Desktop/Teste NL/", c2)
	stop = timeit.default_timer()
	print("End, Runtime:", stop-start)

main()
