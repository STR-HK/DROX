from material_color_utilities_python import *

img = Image.open('Winterly.jpg')
argb = sourceColorFromImage(img)

print(hexFromArgb(argb))