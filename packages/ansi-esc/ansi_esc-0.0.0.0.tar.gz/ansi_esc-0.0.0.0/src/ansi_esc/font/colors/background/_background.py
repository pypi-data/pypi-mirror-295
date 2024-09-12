'''
ANSI escape character definitions for font background color.
'''
from ansi_esc.font.esc import esc
from ansi_esc.font.colors._color_id import validate_color_8_id
from ansi_esc.font.colors._color_id import format_color_256
from ansi_esc.font.colors._color_id import format_color_rgb



def color(id:int):
    validate_color_8_id(id)
    return esc(40+id)

black = color(0)
red = color(1)
green = color(2)
yellow = color(3)
blue = color(4)
magenta = color(5)
cyan = color(6)
white = color(7)

def color_256(id:int):
    return esc("48;" + format_color_256(id))

def color_rgb(r:int, g:int, b:int):
    return esc("48;" + format_color_rgb(r,g,b))

off = default = esc(49)

def color_bright(id:int):
    validate_color_8_id(id)
    return esc(100+id)

black_bright = color_bright(0)
red_bright = color_bright(1)
green_bright = color_bright(2)
yellow_bright = color_bright(3)
blue_bright = color_bright(4)
magenta_bright = color_bright(5)
cyan_bright = color_bright(6)
white_bright = color_bright(7)
