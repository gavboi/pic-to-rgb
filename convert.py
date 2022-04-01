import os, sys, time, math

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
    elif sys.argv[4].lower() in out_conv:
        out_type = out_conv[sys.argv[4].lower()]

# ---process---
print("Pulling from image...\n")
timer = 0
colours1 = []
colours2 = []
colours3 = []
colours4 = []
t = time.time()
im = Image.open(pic)
w, h = im.size
if new_w*new_h == 0: # make this fit better
    new_w, new_h = 20, round(20*h/w)
factor_w, factor_h = w/new_w, h/new_h
img = im.load()
if out_type == DESMOS:
    regions = 2 if new_w*new_h >= 2000 else 1
    for y in range(math.floor(new_h/regions)): 
        for x in range(math.floor(new_w/regions)):
            rgba = img[math.floor(factor_w*(1/2+x)),
                       math.floor(factor_h*(1/2+y))]
            colours1.append((rgba[0], rgba[1], rgba[2]))
    if regions > 1:
        for y in range(math.floor(new_h/regions)): 
            for x in range(math.floor(new_w/regions)):
                rgba = img[math.floor(factor_w*(1/2+x)+w/regions),
                           math.floor(factor_h*(1/2+y))]
                colours2.append((rgba[0], rgba[1], rgba[2]))
        for y in range(math.floor(new_h/regions)): 
            for x in range(math.floor(new_w/regions)):
                rgba = img[math.floor(factor_w*(1/2+x)),
                           math.floor(factor_h*(1/2+y)+h/regions)]
                colours3.append((rgba[0], rgba[1], rgba[2]))
        for y in range(math.floor(new_h/regions)): 
            for x in range(math.floor(new_w/regions)):
                rgba = img[math.floor(factor_w*(1/2+x)+w/regions),
                           math.floor(factor_h*(1/2+y)+h/regions)]
                colours4.append((rgba[0], rgba[1], rgba[2]))
elif out_type == HTML:
    for y in range(new_h):
        colours1.append([])
        for x in range(new_w):
            rgba = img[math.floor(factor_w*(1/2+x)), math.floor(factor_h*(1/2+y))]
            colours1[y].append((rgba[0], rgba[1], rgba[2]))
else: 
    for y in range(new_h): 
        for x in range(new_w):
            rgba = img[math.floor(factor_w*(1/2+x)), math.floor(factor_h*(1/2+y))]
            colours1.append((rgba[0], rgba[1], rgba[2]))

# ---display---
print("Image: {0}".format(pic))
print("Original size: {0}x{1} ({2})".format(w, h, round(w/h, 3)))
print("New size: {0}x{1} ({2})".format(new_w, new_h, round(new_w/new_h, 3)))
print("Size factor: {0}x{1}".format(round(factor_w,3), round(factor_h,3)))
print("Creating output...")
pr = ""
ext = "txt"
if out_type == DESMOS:
    print("(Desmos format)")
    print("Regions: {0}".format(regions))
    if len(colours1) > 2000:
        print("WARNING: Desmos may not accept this length ({0})".format(len(colours1)))
    despre = "S=Calc.getState()\n"
    desc1 = "S.expressions.list[1].latex=\"C_1="
    desc2 = "\"\nS.expressions.list[2].latex=\"C_2="
    desc3 = "\"\nS.expressions.list[3].latex=\"C_3="
    desc4 = "\"\nS.expressions.list[4].latex=\"C_4="
    despost = ("\"\nS.expressions.list[5].latex=\"N={0}" +
               "\"\nS.expressions.list[6].latex=\"W={1}" +
               "\"\nS.expressions.list[7].latex=\"H={2}" +
               "\"\nCalc.setState(S)").format(regions, math.floor(new_w/regions),
                                              math.floor(new_h/regions))
    rgbop = "\\\\operatorname{rgb}"
    pr1 = "\\\\left[ "
    pr2 = "\\\\left[ "
    pr3 = "\\\\left[ "
    pr4 = "\\\\left[ "
    for c in colours1: pr1 += rgbop + str(c) + ","
    for c in colours2: pr2 += rgbop + str(c) + ","
    for c in colours3: pr3 += rgbop + str(c) + ","
    for c in colours4: pr4 += rgbop + str(c) + ","
    pr = (despre + desc1 +
          pr1[:-1].replace(" ","").replace("(", "\\\\left(").replace(")", "\\\\right)") +
          "\\\\right]" + desc2 +
          pr2[:-1].replace(" ","").replace("(", "\\\\left(").replace(")", "\\\\right)") +
          "\\\\right]" + desc3 +
          pr3[:-1].replace(" ","").replace("(", "\\\\left(").replace(")", "\\\\right)") +
          "\\\\right]" + desc4 +
          pr4[:-1].replace(" ","").replace("(", "\\\\left(").replace(")", "\\\\right)") +
          "\\\\right]" + despost)
elif out_type == HTML:
    print("(HTML format)")
    html_head = ("<!DOCTYPE html><html><head><title>" +
                 "{0} {1}x{2}</title></head><style>".format(pic, new_w, new_h) +
                 " .cell{width:20px;height:20px;text-align:center;" +
                 "vertical-align:middle;font-size:6pt;color:#666666;" +
                 "border:0px;font-family:'Arial';white-space:nowrap;" +
                 "cursor:default;} .outer{border:solid 1px #dddddd;}")
    html_body1 = "</style><body><table class=\"tbl\" cellspacing=\"0\"><thead><tr>"
    html_body2 = "</tr></thead><tbody><tr>"
    html_body3 = "</tr><tr>"
    html_body4 = "</tr></tbody></table></body></html>"
    def html_style(i, bgc, tc):
        return (" .s{0}".format(i) + "{background-color:#" +
                "{0};color:#{1};".format(bgc, tc) + "}")
    def html_bodyt(typ, cls, val):
        return "<t{0} class=\"{1}\">{2}</t{0}>".format(typ, cls, val)
    S = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    def b26(i):
        a = math.floor(i/676)
        b = math.floor((i-a*676)/26)
        c = math.floor(i-a*676-b*26)
        if new_h > 25:
            if new_h > 675: return S[a] + S[b] + S[c]
            else: return S[b] + S[c]
        else: return S[c]
    pr1 = ""
    pr2 = html_bodyt("h", "", "")
    pr3 = ""
    i = 0
    j = 0
    for row in colours1:
        pr3 += html_bodyt("h", "cell outer", b26(j)) # pixel row title
        for rgb in row: 
            bgc = (("0" if rgb[0] < 16 else "") + hex(rgb[0])[2:] +
                   ("0" if rgb[1] < 16 else "") + hex(rgb[1])[2:] +
                   ("0" if rgb[2] < 16 else "") + hex(rgb[2])[2:])
            tc = "ffffff" if (rgb[0] + rgb[1] + rgb[2] < 500) else "000000"
            pr1 += html_style(i, bgc, tc) # style
            if j == 0: pr2 += html_bodyt("h", "cell outer", i + 1) # title row
            pr3 += html_bodyt("d", "cell s{0}".format(i), "") # pixel row content
            i += 1
        pr3 += html_body3 # pixel row separator
        j += 1
    pr3 = pr3[:-len(html_body3)]
    pr = (html_head + pr1 + html_body1 + pr2 + html_body2 + pr3 + html_body4)
    ext = "html"
else:
    print("(Standard rgb format)")
    for c in colours1:
        pr += str(c) + "\n"

f = open("out.{0}".format(ext), "w")
f.write(pr)
f.close()
timer = time.time()-t
print("Output saved to out.{0}".format(ext))
print("Completed in {0}s.".format(round(timer, 3), 3))
input("\n([Enter] to close)")
time.sleep(0.2)




















