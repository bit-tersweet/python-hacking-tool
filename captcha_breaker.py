import pytesseract
from urllib import urlretrieve
from PIL import Image

link = input("Enter link of captcha: ")
#getting image from link
urlretrieve(link, 'tmp.png')

#bolding letters:
img = Image.open('temp.png')
img = img.convert("RGBA")
pix = img.load()
for y in xrange(img.size[1]):
    for x in xrange(img.size[0]):
        if pix[x, y][0] < 90:
            pix[x, y] = (0, 0, 0, 255)
for y in xrange(img.size[1]):
    for x in xrange(img.size[0]):
        if pix[x, y][1] < 136:
            pix[x, y] = (0, 0, 0, 255)
for y in xrange(img.size[1]):
    for x in xrange(img.size[0]):
        if pix[x, y][2] > 0:
            pix[x, y] = (255, 255, 255, 255)
img.save("temp.png", "png")


#print the result
print pytesseract.image_to_string(Image.open('temp.png'))
