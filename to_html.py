from PIL import Image
import math
import general_image as gi
from to_type import Template


class Html(Template):


    FORMAT = "HTML"
    EXT = ".html"

    def __init__(self, pic, new_w, new_h):
        self.pic = pic
        self.w, self.h = gi.get_size(pic)
        self.new_w, self.new_h = gi.fix_new(self.w, self.h, new_w, new_h)
        self.factor_w, self.factor_h = gi.get_factors(self.w,
                                                      self.h,
                                                      self.new_w,
                                                      self.new_h)
        self.colours = []
        self.regions = 1

    def pull_rgb(self):
        col = []
        with Image.open(self.pic) as im:
            img = im.load()
            for y in range(self.new_h):
                col.append([])
                for x in range(self.new_w):
                    rgba = img[math.floor(self.factor_w*(1/2+x)),
                               math.floor(self.factor_h*(1/2+y))]
                    col[y].append((rgba[0], rgba[1], rgba[2]))
        self.colours = col

    def generate_out(self):
        html_head = ("<!DOCTYPE html><html><head><title>" +
                     "{0} {1}x{2}</title></head><style>".format(self.pic,
                                                                self.new_w,
                                                                self.new_h) +
                     " .cell{width:20px;height:20px;text-align:center;" +
                     "vertical-align:middle;font-size:6pt;color:#666666;" +
                     "border:0px;font-family:'Arial';white-space:nowrap;" +
                     "cursor:default;} .outer{border:solid 1px #dddddd;}")
        BODY1 = ("</style><body><table class=\"tbl\" " +
                      "cellspacing=\"0\"><thead><tr>")
        BODY2 = "</tr></thead><tbody><tr>"
        BODY3 = "</tr><tr>"
        BODY4 = "</tr></tbody></table></body></html>"

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
            if self.new_h > 25:
                if self.new_h > 675: return S[a] + S[b] + S[c]
                else: return S[b] + S[c]
            else: return S[c]

        sec1 = ""
        sec2 = html_bodyt("h", "", "")
        sec3 = ""
        i = 0
        j = 0
        for row in self.colours:
            # pixel row title
            sec3 += html_bodyt("h", "cell outer", b26(j))
            for rgb in row: 
                bgc = (("0" if rgb[0] < 16 else "") + hex(rgb[0])[2:] +
                       ("0" if rgb[1] < 16 else "") + hex(rgb[1])[2:] +
                       ("0" if rgb[2] < 16 else "") + hex(rgb[2])[2:])
                tc = "ffffff" if (rgb[0] + rgb[1] + rgb[2] < 500) else "000000"
                # style
                sec1 += html_style(i, bgc, tc) 
                # title row
                if j == 0:
                    sec2 += html_bodyt("h", "cell outer", i + 1)
                # pixel row content
                sec3 += html_bodyt("d", "cell s{0}".format(i), "")
                i += 1
            # pixel row separator
            sec3 += BODY3
            j += 1
        sec3 = sec3[:-len(BODY3)]
        print_out = (html_head + sec1 + BODY1 + sec2 + BODY2 + sec3 + BODY4)
        return print_out
        
