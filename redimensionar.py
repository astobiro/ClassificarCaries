import cv2
import glob
import timeit
import numpy as np
import random

def findSmaller(images):
	minWidth = 9999
	minHeight = 9999
	for i in range(len(images)):
		if images[i].shape[0] < minHeight and images[i].shape[1] < minWidth:
			minHeight = images[i].shape[1]
			minWidth = images[i].shape[0]
			minI = i

	return minWidth, minHeight, minI

def preencher(image):
	temp = np.zeros((28, 28), np.uint8)
	width = image.shape[0]
	height = image.shape[1]
	for i in range(width):
		for j in range(height):
			temp[i][j] = image[i][j]

	return temp

def resize(image):
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
	resles = []
	resnonles = []
	for i in range(len(les)):
		tempImg = resize(les[i])
		resles.append(tempImg)

	for i in range(len(nonles)):
		tempImg = resize(nonles[i])
		resnonles.append(tempImg)

	return resles, resnonles

def checkInList(list, el):
	for i in range(len(list)):
		if el == list[i]:
			return True
	return False

def removeElements(list, els):
	newlist = []
	for i in range(len(list)):
		if checkInList(els, i):
			i += 1
		else:
			newlist.append(list[i])

	return newlist

def saveImagesToFolder(images, folder, count):
    counter = count
    print("Start saving:", counter)
    for i in range(len(images)):
        cv2.imwrite(folder + str(counter) + ".jpg", images[i])
        counter += 1
    print("End saving:", counter)
    return counter

def TreinoTeste(les, nonles):
	randles = []
	randnonles = []
	randomles = []
	newrandomles = 0
	randomnonles = []
	newrandomnonles = 0
	for i in range(100):
		newrandomles = random.randint(0, len(les)-1)
		if checkInList(randomles, newrandomles) == False:
			randomles.append(newrandomles)
		else:
			while checkInList(randomles, newrandomles):
				newrandomles = random.randrange(0, len(les)-1)
			randomles.append(newrandomles)

		newrandomnonles = random.randint(0, len(nonles)-1)
		if checkInList(randomnonles, newrandomnonles) == False:
			randomnonles.append(newrandomnonles)
		else:
			while checkInList(randomnonles, newrandomnonles):
				newrandomnonles = random.randrange(0, len(nonles)-1)
			randomnonles.append(newrandomnonles)

		randles.append(les[newrandomles])
		randnonles.append(nonles[newrandomnonles])

	# print(randomles)
	# print(randomnonles)
	treinoles = removeElements(les, randomles)
	treinononles = removeElements(nonles, randomnonles)

	return treinoles, randles, treinononles, randnonles

def rotate(image, angle):
	x, y = image.shape
	M = cv2.getRotationMatrix2D((y/2, x/2), angle, 1)
	dst = cv2.warpAffine(image, M, (y, x))

	return dst

def generate9(image):
	img1 = rotate(image, 90)
	img2 = cv2.flip(rotate(image, 90), 0)
	img3 = cv2.flip(rotate(image, 90), 1)
	img4 = rotate(image, 180)
	img5 = cv2.flip(rotate(image, 180), 0)
	img6 = cv2.flip(rotate(image, 180), 1)
	img7 = rotate(image, 270)
	img8 = cv2.flip(rotate(image, 270), 0)
	img9 = cv2.flip(rotate(image, 270), 1)

	return img1, img2, img3, img4, img5, img6, img7, img8, img9

def rotateAndGenerateAll(trainles, testles, trainnonles, testnonles):
	newtrainles = []
	newtestles = []
	newtrainnonles = []
	newtestnonles = []
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
	#Redimensiona todas as imagens para uma escala 28x28
	reslImages, resnlImages = resizeAll(lImages, nlImages)
	print("Redimensionados: ", len(reslImages), "lesões e", len(resnlImages), "não lesões")

	# cv2.imshow("Teste", reslImages[28])
	# cv2.imshow("Teste 2", reslImages[123])
	# cv2.imshow("Teste 3", resnlImages[123])
	# cv2.imshow("Teste 4", resnlImages[98])
	# cv2.waitKey()

	treinoles, testeles, treinononles, testenonles = TreinoTeste(reslImages, resnlImages)
	print(len(treinoles), len(testeles), len(treinononles), len(testenonles))
	newtrainles, newtrainnonles = rotateAndGenerateAll(treinoles, testeles, treinononles, testenonles)
	print(len(newtrainles), len(newtrainnonles), len(newtrainles) + len(newtrainnonles) + 200)
	random.shuffle(newtrainles)
	random.shuffle(newtrainnonles)
	c = saveImagesToFolder(newtrainles, "C:/Users/Artur/Desktop/Treino L/", 0)
	c1 = saveImagesToFolder(testeles, "C:/Users/Artur/Desktop/Teste L/", c)
	c2 = saveImagesToFolder(newtrainnonles, "C:/Users/Artur/Desktop/Treino NL/", c1)
	c3 = saveImagesToFolder(testenonles, "C:/Users/Artur/Desktop/Teste NL/", c2)
	stop = timeit.default_timer()
	print("End, Runtime:", stop-start)

main()
