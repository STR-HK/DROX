from modules.material_color_utilities_python import *
from MyDependencies.MyAssets import *

img = Image.open(C_SparkleWinter)

theme = themeFromSourceColor(argbFromHex("#6750A4"))
# theme = themeFromSourceColor(sourceColorFromImage(img))

colorMode = "dark"

schemes = theme["schemes"]
lightColorScheme = schemes["light"]
darkColorScheme = schemes["dark"]

colorScheme: Scheme

if colorMode == "light":
    colorScheme = lightColorScheme
else:
    colorScheme = darkColorScheme


# ACCENT_COLOR = "#731D2C"
# ACCENT_COLOR_LIGHT = "#902437"  # 25% Lighter
