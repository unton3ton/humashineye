from PIL import Image, ImageChops

"""
image_1=Image.open('1.jpg')
image_2=Image.open('2.jpg')

result=ImageChops.difference(image_1, image_2)
#result.show()

#Вычисляет ограничивающую рамку ненулевых областей на изображении.
print(result.getbbox()) 

# result.getbbox() в данном случае вернет (0, 0, 888, 666)
result.save('result.jpg')
"""


def difference_images(img1, img2):
    image_1 = Image.open(img1)
    image_2 = Image.open(img2)
    
    size = [400,300]        #размер в пикселях
    image_1.thumbnail(size) #уменьшаем первое изображение
    image_2.thumbnail(size) #уменьшаем второе изображение

    #сравниваем уменьшенные изображения
    result=ImageChops.difference(image_1, image_2)
    
    print(result.getbbox()) 
    
    result.save('result_1.png')

difference_images('norma1_1.png','speckled_1.png')