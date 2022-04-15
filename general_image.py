from PIL import Image


def get_size(pic):
    with Image.open(pic) as im:
        w, h = im.size
    return w, h


def fix_new(w, h, new_w, new_h):
    if new_w*new_h == 0: 
        new_w, new_h = 20, round(20*h / w)
    return new_w, new_h


def get_factors(w, h, new_w, new_h):
    return w/new_w, h/new_h
    
