import cv2
import glob
import timeit
import numpy as np

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

def main():
	print("Start")
	start = timeit.default_timer()
	#Carrega todas as imagens nas pastas em listas
	lImages = [cv2.imread(file, 0) for file in glob.glob("C:/Users/Artur/Dropbox/Projeto/Patches L/*.jpg")]
	nlImages = [cv2.imread(file, 0) for file in glob.glob("C:/Users/Artur/Dropbox/Projeto/Patches NL/*.jpg")]
	#Redimensiona todas as imagens para uma escala 28x28
	reslImages, resnlImages = resizeAll(lImages, nlImages)
	print("Redimensionados: ", len(reslImages), len(resnlImages))

	# cv2.imshow("Teste", reslImages[28])
	# cv2.imshow("Teste 2", reslImages[123])
	# cv2.imshow("Teste 3", resnlImages[123])
	# cv2.imshow("Teste 4", resnlImages[98])
	# cv2.waitKey()

	stop = timeit.default_timer()
	print("End, Runtime:", stop-start)

main()
