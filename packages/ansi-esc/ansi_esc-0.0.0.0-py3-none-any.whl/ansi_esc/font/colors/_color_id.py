'''
Internal module for color id functions.
'''
# Color 8 ID
def validate_color_8_id(id:int):
    if not is_valid_color_8_id(id):
        msg = f"invalid index id (0, 7): {id}"
        raise ValueError(msg)

def is_valid_color_8_id(id:int):
    return not (id < 0 or id > 7)



# Color 256 ID
def format_color_256(id:int):
    validate_color_256_id(id)
    return f"5;{id}"

def validate_color_256_id(id:int):
    if not is_valid_color_256_id(id):
        msg = f"invalid index id (0, 255): {id}"
        raise ValueError(msg)

def is_valid_color_256_id(id:int) -> bool:
    return not (id < 0 or id > 255)



# Color r,g,b
def format_color_rgb(r:int, g:int, b:int):
    validate_color_rgb(r,g,b)
    return "2;"+";".join([str(r), str(g), str(b)])

def validate_color_rgb(r:int, g:int, b:int):
    for value in [r,g,b]:
        if not is_valid_color_256_id(value):
            msg = f"invalid (r, g, b) value (0, 255): ({r}, {g}, {b})"
            raise ValueError(msg)
