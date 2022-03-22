import os, sys, time

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

# ---acquire matplot---
try:
    import matplotlib.pyplot as plt
    print("matplotlib found")
except:
    stream = os.popen('pip install matplotlib')
    output = stream.read()
    print("windows command attempted for acquiring matplotlib\n" + output)
    try:
        import matplotlib.pyplot as plt
        print("matplotlib found")
    except:
        stream = os.popen('python3 -m pip install matplotlib')
        output = stream.read()
        print("linux command attempted for acquiring matplotlib\n" + output)
        try:
            import matplotlib.pyplot as plt
            print("matplotlib found")
        except:
            print("matplotlib could not be found or acquired")
    print("Please restart script.")
    sys.exit()

# ---get images---
pics = []
if len(sys.argv) == 1:
    directory = input("Please specify a path to an image or directory: ")
else:
    directory = sys.argv[1]
if len(directory) == 0:
    directory = os.path.join("samples", "testv_3.mp4")
    print("No file provided. Using default file {0}...".format(directory))
if directory.endswith(".png") or directory.endswith(".jpg"):
    if os.path.isfile(directory):
        pics.append(directory)
    else:
        print("Could not find image.")
        sys.exit()
elif directory.endswith(".mp4") or directory.endswith(".avi"):
    if os.path.isfile(directory):
        if not os.path.isdir("video_frames"):
            print("Making 'video_frames' output folder...")
            os.mkdir("video_frames")
            confirm = "y"
        else:   
            confirm = input("'video_frames' will be overwritten. Is this ok? (y/n) ")
        if confirm.startswith("y"):
            print("Converting video to images...")
            t = time.time()
            for file in os.listdir("video_frames"):
                os.remove(os.path.join("video_frames", file))
            vid = cv2.VideoCapture(directory)
            frame = 0
            fps = 5
            suc = True
            while suc:
                vid.set(cv2.CAP_PROP_POS_MSEC,round(frame*(1/fps)*1000))
                suc, img = vid.read()
                if suc:
                    #img = ~img #invert
                    name = os.path.join("video_frames", "{0}.jpg".format(frame))
                    cv2.imwrite(name, img)
                    pics.append(name)
                frame += 1
            t = time.time() - t
            print("Video converted to images at {1} fps in {0}s.".format(t, fps))
        else:
            print("Please deal with the existing files and try again.")
            sys.exit()
    else:
        print("Could not find video.")
        sys.exit()
else:
    if os.path.isdir(directory):
        for file in os.listdir(directory):
            if file.endswith(".png") or file.endswith(".jpg"):
                pics.append(os.path.join(directory, file))
    else:
        print("Could not find directory.")
        sys.exit()
print("{0} images found. Processing...".format(len(pics)))

# ---iterate/process---
lums = []
times = []
for p in pics: # iterates per picture uploaded
    t = time.time()
    im = Image.open(p)
    lum = 0
    w, h = im.size
    img = im.load()
    for x in range(w): # iterates across x
        for y in range(h): # iterates across y
            rgba = img[x,y]  # Set the RGBA Value of the image (tuple)
            lum += (0.2126*rgba[0] + 0.7152*rgba[1] + 0.0722*rgba[2])
    lums.append(lum)
    times.append(round(time.time()-t,3))
    print("(Progress: {2}/{3}) {0} completed in {1}s.".format(p, times[-1], len(lums), len(pics)))

# ---display---
print("Completed in {0}s.".format(round(sum(times),3)))
plt.plot([round(i/fps,2) for i in range(len(pics))], lums, color='black', marker='o', linestyle='dashed')
plt.title("Luminance by frame ({0})".format(directory))
plt.xlabel("Time (s)")
plt.ylabel("Total Brightness in Frame")
plt.show()
