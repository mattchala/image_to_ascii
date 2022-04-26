from PIL import Image, ImageFilter
import time

chars = ["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", "."]
char_div = 25

def set_shade(num):
    global chars
    global char_div
    if num == 11:
        chars = ["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", "."]
        char_div = 25
    if num == 10:
        chars = ["@", "$", "%", "?", "*", "+", ";", ":", ",", "."]
        char_div = 27
    if num == 9:
        chars = ["@", "$", "%", "?", "*", ";", ":", ",", "."]
        char_div = 30 
    if num == 8:
        chars = ["@", "$", "%", "?", "*", ";", ",", "."]
        char_div = 35
    if num == 7:
        chars = ["@", "$", "%", "?", "*", ";", "."]
        char_div = 40
    if num == 6:
        chars = ["@", "%", "?", "*", ";", "."]
        char_div = 50
    if num == 5:
        chars = ["@", "%", "?", ";", "."]
        char_div = 60
    if num == 4:
        chars = ["@", "?", ";", "."]
        char_div = 65
    if num == 3:
        chars = ["@", "?", "."]
        char_div = 90
    if num == 2:
        chars = ["@", "."]
        char_div = 140

def resize(image, new_width):
    stretch_correction = 0.55
    width, height = image.size
    new_height = new_width * height / width * stretch_correction
    new_height = int(new_height)
    return image.resize((new_width, new_height))
 
def make_gray(image):
    return image.convert("L")

def to_ascii_str(image):
    pix = image.getdata()
    ascii_str = ""
    for p in pix:
        ascii_str += chars[p//char_div] 
    return ascii_str

def add_new_lines(ascii_str, img_width):
    new_txt_img = ""
    str_len = len(ascii_str)
    for i in range(0, str_len, img_width):
        new_txt_img += ascii_str[i : i + img_width] + "\n"
    return new_txt_img

def set_contrast(image, value):
    return image.filter(ImageFilter.UnsharpMask(value))


while True:
    time.sleep(1.0)  # maybe not needed?

    # initialize user modifiable vars
    path = ""
    scale_val = 10
    contrast_val = 0
    shade_val = 0

    # get vars from txt
    var_txt = open("vars.txt", "r+")
    var_lines = var_txt.readlines()
    cur = 0
    for line in var_lines:
        cur += 1
        if cur == 1:
            path = line.strip()
        elif cur == 2:
            scale_val = int(line.strip())
        elif cur == 3:
            contrast_val = int(line.strip())
        elif cur == 4:
            shade_val = int(line.strip())
    var_txt.close()

    try:
        image = Image.open(path)
    except:
        print(path, "Unable to find image ")

    image = resize(image, scale_val)   
    grey_image = make_gray(image)
    grey_image = set_contrast(grey_image, contrast_val)
    set_shade(shade_val)  
    ascii_str = to_ascii_str(grey_image)
    ascii_image = add_new_lines(ascii_str, grey_image.width)

    # open & save this file to new file with user specified name & dir path
    with open("ascii_output.txt", "w") as output:
        output.write(ascii_image)
