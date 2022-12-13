from PIL import Image, ImageChops
import cv2

def blur_image(img):
    image = cv2.imread(img)
    result = cv2.blur(image, (6,6))
    cv2.imwrite(f'{img}_blur.png', result)

def difference_images(img1, img2):
    image_1 = Image.open(img1).convert('L')
    image_2 = Image.open(img2).convert('L')
    
    # size = [400,300]        #размер в пикселях
    # image_1.thumbnail(size) #уменьшаем первое изображение
    # image_2.thumbnail(size) #уменьшаем второе изображение

    # работает сравнение только при одинаковых размерах изображений
    # делаем размер сравниваемого изображения равным изображению нормы
    width, height = image_1.size
    newsize = (width, height)
    image_2 = image_2.resize(newsize)

    #сравниваем уменьшенные изображения
    result=ImageChops.difference(image_1, image_2)#.getbbox() 
    result.show()

    #Вычисляет ограничивающую рамку ненулевых областей на изображении.
    print(result.getbbox()) # можно использовать для классификации

    # result.getbbox() в данном случае вернет (0, 0, 888, 666)
    result.save('result1.jpg')


# difference_images("focal.jpg","norma1.jpg")

# blur_image('focal.jpg')
# blur_image('norma1.jpg')
difference_images("result0.jpg","norma_mirror.png")