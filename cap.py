from PIL import Image

# Открываем изображение
img = Image.open("Screenshot_5.png")


pixels = img.load()
pixels[25, 10]



bad_colors = [(64, 64, 64), (0,0,255)]

for y in range(img.size[1]):
    for x in range(img.size[0]):
        if pixels[x,y] in bad_colors:
            pixels[x,y]
            print(img)


