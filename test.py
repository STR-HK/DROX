from modules.material_color_utilities_python import *
import json

theme = themeFromSourceColor(argbFromHex('#4285f4'))

schemes = theme['schemes']
palettes = theme['palettes']

light = schemes['light']
dark = schemes['dark']

primary = palettes['primary']
secondary = palettes['secondary']
tertiary = palettes['tertiary']
neutral = palettes['neutral']
neutralVariant = palettes['neutralVariant']
error = palettes['error']

print(light)
print(dark)
print('-----')
print(primary)
print(secondary)
print(tertiary)
print(neutral)
print(neutralVariant)
print(error)