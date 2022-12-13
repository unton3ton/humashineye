

from pathlib import Path
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image, ImageDraw, ImageFont
import cv2
import numpy as np
from matplotlib import pyplot as plt
import imagehash 
import os


def index_max(arr, n): # определяет пигментацию
	arr1 = arr.copy()
	b = []
	for i in range(n+1):
		ind = np.argmax(arr1, axis=0)
		b.append(ind[0])
		arr1[ind] *= -1
	b = sorted(b)
	return b

def distant_pigment(a, b): # определяет HAF-расстояние в пространстве пигментации
	s = 0
	dist = list(abs(np.array(a) - np.array(b)))
	for i in range(len(dist)-1, 0, -1):
		s += dist[i]
	return(int(s/len(dist)))

def distant_hash(photo, photo1):
# вычисляем HASH-расстояние между фотоизображениями
	hash_img = imagehash.average_hash(Image.open(photo))
	hash_img1 = imagehash.average_hash(Image.open(photo1))
	return abs(hash_img - hash_img1)

def predict(a, b):
	if(((0<=a<=3) or (8<=a<=12)) and (0<=b<=3)):
		return "норма"
	elif((22<=a<=36) and (4<=b<=6)):
		return "минимальные изменения"
	elif((16<=a<=30) and (9<=b<=12)):
		return "фокальная"
	elif((5<=a<=11) and (10<=b<=13)):
		return "пятнистая"
	elif((4<=a<=18) and (4<=b<=7)):
		return "линейная"
	elif((a > 37) and (b > 10)):
		return "кружевная"
	elif((21<=a<=35) and (8<=b<=13)):
		return "ретикулярная"
	elif((10<=a<=22) and (8<=b<=11)):
		return "крапчатая"
	else:
		return "уточните прогноз с другой нормой"

def distances(photo, photo1):
	# вычисляем HAF-расстояние между фотоизображениями
	img = cv2.imread(photo)
	img1 = cv2.imread(photo1)
	BLU = 6 # окно размытия
	img = cv2.blur(img, (BLU,BLU))
	img1 = cv2.blur(img1, (BLU,BLU))

	hist = cv2.calcHist([img],[0],None,[256],[1,256])
	hist1 = cv2.calcHist([img1],[0],None,[256],[1,256])

	n = 100 # ширина интервала около максимума гистограммы

	print(f"прогноз: {predict(distant_pigment(index_max(hist, n), index_max(hist1, n)), distant_hash(photo, photo1))}")
	
	# строим графики рассеяния: гистограммы сравниваемых изображений
	x = np.arange(1, 257) 
	plt.scatter(x, hist, label = "норма") # photo[:-4]) 
	plt.scatter(x, hist1, label = f"прогноз: {predict(distant_pigment(index_max(hist, n), index_max(hist1, n)), distant_hash(photo, photo1))}") # photo1[:-4])

	plt.legend()
	plt.xlabel('Яркость пикселя', fontsize=15)
	plt.ylabel('Число пикселей', fontsize=15)
	plt.grid(True)
	plt.title(f'HAF-расстояние = {distant_pigment(index_max(hist, n), index_max(hist1, n))}, HASH-расстояние = {distant_hash(photo, photo1)}')
	plt.savefig(f'blur histograms for {photo[:-4]} & {photo1[:-4]}')
	plt.show()


root = Tk()

current_dir = Path.cwd()

#x_size_screen = int(root.winfo_screenwidth()/3)
y_size_screen = int(root.winfo_screenheight()/3)

x_size_root = int(y_size_screen*1.5)
y_size_root = int(y_size_screen*1.5)

root.geometry('{}x{}'.format(x_size_root,y_size_root)) 

canvas = Canvas(root,width=y_size_screen,height=y_size_screen)
canvas.pack()

photo = 'norma1.jpg' # заданное фото условной нормы для демонстрации
filename = None
new_norm_path = None
new_norm = 'norma1.jpg' # заданное фото условной нормы для расчётов


image = Image.open(photo).convert('L')
old_size_x, old_size_y = image.size[0], image.size[1]
image = image.resize((y_size_screen,y_size_screen)) 

if filename == None:
	draw = ImageDraw.Draw(image) # для отрисовки текста на изображении
	front_size = 25
	font = ImageFont.truetype("san-serif.ttf", front_size) # параметры текста
	draw.text((0, 0), "Текущая норма", 255,font=font) # наносим текст на изображение
else:
	pass

pilimage = ImageTk.PhotoImage(image)
imagesprite = canvas.create_image(0,0,image=pilimage, anchor=NW)

container = Frame() # создаём контейнер на главном окне для расположения кнопок и полей ввода
container.pack(side='top', fill='both', expand=True)

###################################################################################
def my_callback1(): # 
	global filename
	filename = filedialog.askopenfilename(initialdir = current_dir, \
 				title = "Select imagefile", filetypes = (("jpg files", "*.jpg"),\
 					("jpeg files", "*.jpeg"),
 										("JPG files", "*.JPG"),("png files", "*.png"),
 										("bmp files", "*.bmp"),("all files", "*.*")))
	global image
	image = Image.open(filename).convert('L')
	image = image.resize((y_size_screen,y_size_screen))
	global pilimage
	pilimage = ImageTk.PhotoImage(image)
	global imagesprite
	imagesprite = canvas.create_image(0,0,image=pilimage, anchor=NW)

button1 = Button(container , text="Выбрать фотоизображение" , command=my_callback1)
button1.grid(row=1 ,column=0)
###################################################################################

###################################################################################
def my_callback2(): # 
	global new_norm_path
	new_norm_path = filedialog.askopenfilename(initialdir = current_dir, \
 				title = "Select imagefile", filetypes = (("jpg files", "*.jpg"),\
 					("jpeg files", "*.jpeg"), ("JPG files", "*.JPG"),("png files", "*.png"),
 										("bmp files", "*.bmp"),("all files", "*.*")))
	new_norm = Image.open(new_norm_path).convert('L')
	#new_norm.show()

	global filename
	filename = filedialog.askopenfilename(initialdir = current_dir, \
 				title = "Select imagefile", filetypes = (("jpg files", "*.jpg"),\
 					("jpeg files", "*.jpeg"), ("JPG files", "*.JPG"),("png files", "*.png"),
 										("bmp files", "*.bmp"),("all files", "*.*")))
	global image
	image = Image.open(filename).convert('L')
	image = image.resize((y_size_screen,y_size_screen))

	global pilimage
	pilimage = ImageTk.PhotoImage(image)
	global imagesprite
	imagesprite = canvas.create_image(0,0,image=pilimage, anchor=NW)

button2 = Button(container , text="Выбрать новую норму и фотоизображение" , command=my_callback2)
button2.grid(row=1 ,column=1)
###################################################################################

###################################################################################
def my_callback3(): # 
	global filename
	if filename == None:
		print("Фото ещё не выбрано")
	else:
		global image
		image = image.transpose(Image.FLIP_LEFT_RIGHT)
		image = image.resize((old_size_x, old_size_y))
		image.save(f"{filename[:-4]}_mirror.jpg")
		image = image.resize((y_size_screen,y_size_screen))
		global pilimage
		pilimage = ImageTk.PhotoImage(image)
		global imagesprite
		imagesprite = canvas.create_image(0,0,image=pilimage, anchor=NW)
		filename = f"{filename[:-4]}_mirror.jpg"
		
button3 = Button(container , text="Отразить выбранное фото по вертикали" , command=my_callback3)
button3.grid(row=3 ,column=0)
###################################################################################

###################################################################################
def my_callback4(): # 
	global filename
	global new_norm_path
	if filename == None:
		print("Фото ещё не выбрано")
	else:
		if new_norm_path == None:
			print("Новая норма ещё не выбрана")
			distances(new_norm, filename.split('/').pop())
		else:
			print("Результат с новой нормой")
			distances(new_norm_path.split('/').pop(), filename.split('/').pop())

button4 = Button(container , text="Классифицировать" , command=my_callback4)
button4.grid(row=3 ,column=1)
###################################################################################

###################################################################################
# def my_callback5(): # 
# 	pass

# button5 = Button(container , text="Уточнить результат" , command=my_callback5)
# button5.grid(row=5 ,column=0)
###################################################################################


root.mainloop()