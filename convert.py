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
new_w = -1
new_h = -1

print("")
if len(sys.argv) > 1:
    pic = sys.argv[1]
while not (os.path.isfile(pic) and (pic.endswith(".png") or pic.endswith(".jpg"))):
    print("No image found.")
    pic = input("Please specify a path to an image (leave blank for auto): ")
    if len(pic) == 0: pic = os.path.join("samples", "test.jpg")
print("")
if len(sys.argv) == 4 and sys.argv[2].isnumeric() and sys.argv[3].isnumeric():
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
    new_w, new_h = 20, round(20*h/w)
factor_w, factor_h = w/new_w, h/new_h
img = im.load()
for y in range(new_h): 
    for x in range(new_w):
        rgba = img[math.floor(factor_w*(1/2+x)), math.floor(factor_h*(1/2+y))]
        colours.append((rgba[0], rgba[1], rgba[2]))

# ---display---
print("Image: {0}".format(pic))
print("Original size: {0}x{1} ({2})".format(w, h, w/h))
print("New size: {0}x{1} ({2})".format(new_w, new_h, new_w/new_h))
print("Size factor: {0}x{1}".format(factor_w, factor_h))
if len(colours) > 10000: print("WARNING: Desmos will not accept lists of over 10000")
desmos = True
despre = "S=Calc.getState()\nS.expressions.list[1].latex=\"C="
despost = "\"\nCalc.setState(S)"
desform = "\\\\operatorname{rgb}" if desmos else ""
pr = "["
for c in colours: pr += desform + str(c) + ","
if desmos:
    pr = (despre + "\\\\left" +
          pr[:-1].replace(" ","").replace("(", "\\\\left(").replace(")", "\\\\right)") +
          "\\\\right]" + despost)
else: pr = pr[:-1] + "]"
f = open("out.txt", "w")
f.write(pr)
f.close()
timer = time.time()-t
print("Output saved to out.txt")
print("Completed in {0}s.".format(round(timer, 3), 3))
input("\n([Enter] to close)")
time.sleep(0.2)
