import os, sys, time, math
from to_html import Html
from to_desmos import Desmos
import general_image as gi

# For desmos, use this graph: https://www.desmos.com/calculator/3wzqhr9vmi

# ---importing pillow---
try: from PIL import Image
except:
    print("Missing required library. Please install pillow.")
    time.sleep(3)
    sys.exit()

DESMOS = 0
HTML = 1
out_conv = {
    "desmos": 0,
    "des": 0,
    "html": 1,
    "grid": 1,
    "txt": 9,
    "plain": 9
    }

# ---get images---
pic = ""
new_w = -1
new_h = -1
out_type = -1

print("")
if len(sys.argv) > 1:
    pic = sys.argv[1]
while not (os.path.isfile(pic) and (pic.endswith(".png") or pic.endswith(".jpg"))):
    print("No image found.")
    pic = input("Please specify a path to an image (leave blank for auto): ")
    if len(pic) == 0: pic = os.path.join("samples", "test.jpg")
print("")
if len(sys.argv) > 3 and sys.argv[2].isnumeric() and sys.argv[3].isnumeric():
    new_w, new_h = int(sys.argv[2]), int(sys.argv[3])
while new_w < 0:
    print("No dimensions found.")
    size = input("Please specify width and height (leave blank for auto): ")
    if len(size) == 0: new_w, new_h = 0, 0
    else:
        size = size.replace(" ",",").replace(",,",",").split(",")
        if len(size) > 1 and size[0].isnumeric() and size[1].isnumeric():
            new_w, new_h = int(size[0]), int(size[1])
print("")
if len(sys.argv) > 4 and sys.argv[4].lower() in out_conv:
    out_type = out_conv[sys.argv[4].lower()]
while out_type < 0:
    print("No output type found.")
    out = input("Please specify output type from list (leave blank for auto) - \n[desmos, html, txt]: ")
    if len(out) == 0: out_type = 9
    elif out in out_conv:
        out_type = out_conv[out]

# ---process---
print("Pulling from image...\n")
timer = 0
t = time.time()

formatter = None
if out_type == DESMOS:
    formatter = Desmos(pic, new_w, new_h)
elif out_type == HTML:
    formatter = Html(pic, new_w, new_h)
else: 
    raise ValueError("Formatter not found.")

formatter.pull_rgb()

# ---display---
print("Image: {0}".format(pic))
print("Original size: {0}x{1} ({2})"
      .format(formatter.w,
              formatter.h,
              round(formatter.w/formatter.h, 3)))
print("New size: {0}x{1} ({2})"
      .format(formatter.new_w,
              formatter.new_h,
              round(formatter.new_w/formatter.new_h, 3)))
print("Size factor: {0}x{1}".format(round(formatter.factor_w, 3),
                                    round(formatter.factor_h, 3)))
print("Regions: {0}".format(formatter.regions))
print("Format: {0}".format(formatter.FORMAT))
print("Creating output...\n")

print_out = formatter.generate_out()
with open("out{0}".format(formatter.EXT), "w") as file:
    file.write(print_out)

timer = time.time()-t
print("Output saved to out{0}".format(formatter.EXT))
print("Completed in {0}s.".format(round(timer, 3), 3))
input("\n([Enter] to close)")
time.sleep(0.2)




















