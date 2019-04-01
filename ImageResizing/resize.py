from PIL import Image
import os
os.getcwd()
allimages = os.listdir()
images=[]
for i in allimages:
    if i.endswith('.jpg'):
        images.append(i)
    continue

len(images)

def resizehalf(img):
    im = Image.open(img)
    im = im.resize((40, 40), Image.ANTIALIAS) # the tuple is the desired resize dimension
    im.save(os.getcwd()+'/resized/'+img)

for i in images:
    resizehalf(i)

