from PyQt5.QtGui import QPixmap
from lxml import etree

import MyDependencies

def change_color(path, color):
    tree = etree.parse(path)
    root = tree.getroot()
    root.set("fill", color)
    # root.set("height", "28")
    # root.set("width", "28")
    # tree.write(path, pretty_print=True)
    xml = etree.tostring(root, pretty_print=True)
    return xml

def change_icon_color(icon, color):
    pix = QPixmap()
    pix.loadFromData(MyDependencies.SvgEditor.change_color(icon, color))
    return pix