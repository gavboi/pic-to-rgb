from PIL import Image
import math
import general_image as gi
from to_type import Template


class Desmos(Template):


    FORMAT = "Desmos"
    EXT = ".txt"
    MAX_REGIONS = 2

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
        colours1 = []
        colours2 = []
        colours3 = []
        colours4 = []
        self.colours = []
        self.regions = 2 if self.new_w*self.new_h >= 2000 else 1
        with Image.open(self.pic) as im:
            img = im.load()
            for y in range(math.floor(self.new_h/self.regions)): 
                for x in range(math.floor(self.new_w/self.regions)):
                    rgba = img[math.floor(self.factor_w*(1/2+x)),
                               math.floor(self.factor_h*(1/2+y))]
                    colours1.append((rgba[0], rgba[1], rgba[2]))
            self.colours.append(colours1)
            if self.regions > 1:
                for y in range(math.floor(self.new_h/self.regions)): 
                    for x in range(math.floor(self.new_w/self.regions)):
                        rgba = img[math.floor(self.factor_w*(1/2+x)+self.w/self.regions),
                                   math.floor(self.factor_h*(1/2+y))]
                        colours2.append((rgba[0], rgba[1], rgba[2]))
                for y in range(math.floor(self.new_h/self.regions)): 
                    for x in range(math.floor(self.new_w/self.regions)):
                        rgba = img[math.floor(self.factor_w*(1/2+x)),
                                   math.floor(self.factor_h*(1/2+y)+self.h/self.regions)]
                        colours3.append((rgba[0], rgba[1], rgba[2]))
                for y in range(math.floor(self.new_h/self.regions)): 
                    for x in range(math.floor(self.new_w/self.regions)):
                        rgba = img[math.floor(self.factor_w*(1/2+x)+self.w/self.regions),
                                   math.floor(self.factor_h*(1/2+y)+self.h/self.regions)]
                        colours4.append((rgba[0], rgba[1], rgba[2]))
        self.colours.append(colours2)
        self.colours.append(colours3)
        self.colours.append(colours4)

    def generate_out(self):
        if len(self.colours[0]) > 2000:
            print("WARNING: Desmos may not accept this length ({0})"
                  .format(len(self.colours[0])))
        desc_n = ["S.expressions.list[1].latex=\"C_1="]
        for i in range(self.MAX_REGIONS**2 - 1):
            desc_n.append("\"\nS.expressions.list[{0}].latex=\"C_{0}="
                          .format(i+2))
        despost = (("\"\nS.expressions.list[{0}].latex=\"N={3}" +
                    "\"\nS.expressions.list[{1}].latex=\"W={4}" +
                    "\"\nS.expressions.list[{2}].latex=\"H={5}" +
                    "\"\nCalc.setState(S)")
                    .format(self.MAX_REGIONS**2 + 1,
                           self.MAX_REGIONS**2 + 2,
                           self.MAX_REGIONS**2 + 3,
                           self.regions,
                           math.floor(self.new_w/self.regions),
                           math.floor(self.new_h/self.regions)))
        RGB_OP = "\\\\operatorname{rgb}"
        col_n = []
        for i in range(self.MAX_REGIONS**2):
            col_n.append("\\\\left[ ")
            if i < len(self.colours):
                for c in self.colours[i]:
                    col_n[i] += RGB_OP + str(c) + ","
        print_out = "S=Calc.getState()\n"
        for i in range(self.MAX_REGIONS**2):
            print_out += (desc_n[i] +
                          col_n[i][: -1].replace(" ","").replace("(", "\\\\left(")
                          .replace(")", "\\\\right)") + "\\\\right]")
        print_out += despost
        return print_out
        
