'''
ANSI escape character definitions for font effects.
'''
from ansi_esc.font.esc import esc



reset = default = normal = esc(0)
bold = increased_intensity = esc(1)
faint = dim = decreased_intensity = esc(2)
italic = esc(3)
underline = singly_underlined = esc(4)
blink = blink_slow = esc(5)
blink_rapid = esc(6)
reverse = inverse = negative = swap_fg_bg = esc(7)
hidden = invisible = conceal = esc(8)
strikethrough = crossout = esc(9)
primary_font = esc(10)

def alt_font(index:int):
    if (index < 0 or index > 8):
        raise ValueError(f"index out of range (0-8): {index}")
    return esc(11 + index)
alt_font_first = alt_font(0)
alt_font_second = alt_font(1)
alt_font_third = alt_font(2)
alt_font_fourth = alt_font(3)
alt_font_fifth = alt_font(4)
alt_font_sixth = alt_font(5)
alt_font_seventh = alt_font(6)
alt_font_eighth = alt_font(7)
alt_font_ninth = alt_font(8)


fraktur = gothic = esc(20)
double_underline = esc(21)
reset_intensity = bold_off = faint_off = dim_off = esc(22)
italic_off = esc(23)
underline_off = esc(24)
blink_off = esc(25)
reverse_off = inverse_off = positive = swap_fg_bg_off = esc(27)
hidden_off = invisible_off = reveal = esc(28)
strikethrough_off = crossout_off = esc(29)
framed = esc(51)
encircled = esc(52)
overlined = esc(53)
framed_and_encircled_off = esc(54)
overlined_off = esc(55)
