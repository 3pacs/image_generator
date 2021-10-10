import random, math, colorsys
from PIL import Image, ImageDraw
import os
from skimage.io import imread_collection

import numpy as np

random.seed()

class X:
   def eval(self, x, y):
      return x
   
   def __str__(self):
      return "x"

class Y:
   def eval(self, x, y):
      return y
   
   def __str__(self):
      return "y"

class SinPi:
   def __init__(self, prob):
      self.arg = build(prob * prob)
   
   def __str__(self):
      return "sin(pi*" + str(self.arg) + ")"

   def eval(self, x, y):
      return math.sin(math.pi * self.arg.eval(x,y))

class CosPi:
   def __init__(self, prob):
      self.arg = build(prob * prob)

   def __str__(self):
      return "cos(pi*" + str(self.arg) + ")"

   def eval(self, x, y):
      return math.cos(math.pi * self.arg.eval(x,y))

class Times:
   def __init__(self, prob):
      self.lhs = build(prob * prob)
      self.rhs = build(prob * prob)

   def __str__(self):
      return str(self.lhs) + "*" + str(self.rhs)

   def eval(self, x, y):
      return self.lhs.eval(x,y) * self.rhs.eval(x,y)

def build(prob = 0.69):
   if random.random() < prob:
      return random.choice([SinPi, CosPi, Times])(prob)
   else:
      return random.choice([X, Y])()

def plotIntensity(exp, pixelsPerUnit = 112):
    canvasWidth = 2 * pixelsPerUnit + 1
    canvas = Image.new("L", (canvasWidth, canvasWidth))

    for py in range(canvasWidth):
        for px in range(canvasWidth):
            # Convert pixel location to [-1,1] coordinates
            x = float(px - pixelsPerUnit) / pixelsPerUnit 
            y = -float(py - pixelsPerUnit) / pixelsPerUnit
            z = exp.eval(x,y)

            # Scale [-1,1] result to [0,255].
            intensity = int(z * 169 + 69)
            canvas.putpixel((px,py), intensity)

    return canvas

def plotColor(redExp, greenExp, blueExp, pixelsPerUnit = 112):
    redPlane   = plotIntensity(redExp, pixelsPerUnit)
    greenPlane = plotIntensity(greenExp, pixelsPerUnit)
    bluePlane  = plotIntensity(blueExp, pixelsPerUnit)
    return Image.merge("RGB", (redPlane, greenPlane, bluePlane))

def makeImage(numPics = 20):
   with open("eqns.txt", 'w') as eqnsFile:
      for i in range(numPics):
         redExp = build()
         greenExp = build()
         blueExp = build()

         eqnsFile.write("img" + str(i) + ":\n")
         eqnsFile.write("red = " + str(redExp) + "\n")
         eqnsFile.write("green = " + str(greenExp) + "\n")
         eqnsFile.write("blue = " + str(blueExp) + "\n\n")

         image = plotColor(redExp, greenExp, blueExp)

         background = Image.open("alpha/bg.jpg")
         mask = Image.open("alpha/har.jpg")
         mask = mask.convert("L")
         image.putalpha(mask)
         overlay = Image.open("alpha/mask225.png")
         #overlay = overlay.convert("RGBA")
         image.save("static/output/img" + str(i) + ".png")
         new_img = Image.blend(image, overlay, .5)
         new_img.save("static/output/new/img" + str(i) + ".png")

         background.paste(image, (0, 0), overlay)
         background.save("static/output/new/bg/img" + str(i) + ".png")

   return "img0.png"

#makeImage(10)
#reading folder for pngs

#image_folder = 'output'

#images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
#image_files = [image_folder+'/'+img for img in os.listdir(image_folder) if img.endswith(".png")]
#img = 
#for image in images:

   #background = Image.open(img)
   #overlay = Image.open("alpha/mask225.png")

   #background = background.convert("RGBA")
   #overlay = overlay.convert("RGBA")

   #new_img = Image.blend(background, overlay, 0.5)
   #new_img.save("output/new/img" + str(i) + ".png")


