import os, sys, time, math

# ---acquire pillow---
try:
    from PIL import Image
    print("pillow found")
except:
    stream = os.popen('pip install pillow')
    output = stream.read()
    print("windows command attempted for acquiring pillow\n" + output)
    try:
        from PIL import Image
        print("pillow found")
    except:
        stream = os.popen('python3 -m pip install pillow')
        output = stream.read()
        print("linux command attempted for acquiring pillow\n" + output)
        try:
            from PIL import Image
            print("pillow found")
        except:
            print("pillow could not be found or acquired")
    print("Please restart script.")
    sys.exit()

# ---acquire opencv---
try:
    import cv2
    print("opencv found")
except:
    stream = os.popen('pip install opencv-python')
    output = stream.read()
    print("windows command attempted for acquiring opencv\n" + output)
    try:
        import cv2
        print("opencv found")
    except:
        stream = os.popen('python3 -m pip install opencv-python')
        output = stream.read()
        print("linux command attempted for acquiring opencv\n" + output)
        try:
            import cv2
            print("opencv found")
        except:
            print("opencv could not be found or acquired")
    print("Please restart script.")
    sys.exit()

# ---get images---
pic = ""
if len(sys.argv) == 1: directory = input("Please specify a path to an image or directory: ")
else: directory = sys.argv[1]
if len(sys.argv) == 4: new_w, new_h = sys.argv[2], sys.argv[3]
else:
    size = input("Please specify width and height (leave blank for auto): ")
    size = size.replace(" ",",").replace(",,",",").split(",")
    if len(size) > 1 and size[0].isnumeric() and size[2].isnumeric():
        new_w, new_h = size[0], size[1]
    else: new_w, new_h = 0, 0
if len(directory) == 0:
    directory = os.path.join("samples", "test.jpg")
    print("No file provided. Using default file {0}...".format(directory))
if directory.endswith(".png") or directory.endswith(".jpg"):
    if os.path.isfile(directory):
        pic = directory
    else:
        print("Could not find image.")
        sys.exit()
##elif directory.endswith(".mp4") or directory.endswith(".avi"):
##    if os.path.isfile(directory):
##        if not os.path.isdir("video_frames"):
##            print("Making 'video_frames' output folder...")
##            os.mkdir("video_frames")
##            confirm = "y"
##        else:   
##            confirm = input("'video_frames' will be overwritten. Is this ok? (y/n) ")
##        if confirm.startswith("y"):
##            print("Converting video to images...")
##            t = time.time()
##            for file in os.listdir("video_frames"):
##                os.remove(os.path.join("video_frames", file))
##            vid = cv2.VideoCapture(directory)
##            frame = 0
##            fps = 5
##            suc = True
##            while suc:
##                vid.set(cv2.CAP_PROP_POS_MSEC,round(frame*(1/fps)*1000))
##                suc, img = vid.read()
##                if suc:
##                    #img = ~img #invert
##                    name = os.path.join("video_frames", "{0}.jpg".format(frame))
##                    cv2.imwrite(name, img)
##                    pics.append(name)
##                frame += 1
##            t = time.time() - t
##            print("Video converted to images at {1} fps in {0}s.".format(t, fps))
##        else:
##            print("Please deal with the existing files and try again.")
##            sys.exit()
##    else:
##        print("Could not find video.")
##        sys.exit()
print("Processing...")

# ---process---
timer = 0
colours = []
t = time.time()
im = Image.open(pic)
w, h = im.size
if new_w*new_h == 0: # make this fit better
    new_w, new_h = 80, 80
factor_w, factor_h = math.floor(w/new_w), math.floor(h/new_h)
img = im.load()
for y in range(new_h): 
    for x in range(new_w):
        rgba = img[x,y]
        colours.append((rgba[0], rgba[1], rgba[2]))
timer = time.time()-t

# ---display---
print("Completed in {0}s.".format(math.floor(timer),3))
if len(colours) > 10000: print("WARNING: Desmos will not accept lists of over 10000")
pr = "["
for c in colours: pr += "rgb" + str(c) + ","
pr = pr[:-1] + "]"
print("--------\n{0}".format(pr))
input("")
time.sleep(1)
