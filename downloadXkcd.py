#! python3
# downloadXkcd.py - Downloads every XKCD comic and title text and combines into one image per comic

import requests, os, bs4
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import textwrap

url = 'http://xkcd.com'             # starting url
os.makedirs('xkcd', exist_ok=True)  # store comics in ./xkcd
while not url.endswith('#'):
    # Download the page.
    print('Downloading page %s...' % url)
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text)
    # Find the URL of the comic image.
    comicElem = soup.select('#comic img')
    if len(comicElem):
        comicTitle = comicElem[0].get('title')
    else:
        comicTitle=''
    if comicElem == []:
         print('Could not find comic image.')
    else:
         try:
             comicUrl = 'http:' + comicElem[0].get('src')
             # Download the image.
             print('Downloading image %s...' % (comicUrl))
             res = requests.get(comicUrl)
             res.raise_for_status()
         except requests.exceptions.MissingSchema:
             # skip this comic
             prevLink = soup.select('a[rel="prev"]')[0]
             url = 'http://xkcd.com' + prevLink.get('href')
             continue

         # Save the image to ./xkcd.
         imageFile = open(os.path.join('xkcd', os.path.basename(comicUrl)), 'wb')
         for chunk in res.iter_content(100000):
             imageFile.write(chunk)
         imageFile.close()
         
         #--------------------COMBINE IMAGE AND TITLE TEXT
         # get an image
         if os.path.basename(comicUrl)!='lyrics.png':
             base = Image.open(os.path.join('xkcd', os.path.basename(comicUrl))).convert('RGBA')
         else:
             prevLink = soup.select('a[rel="prev"]')[0]
             url = 'http://xkcd.com' + prevLink.get('href')
             continue
        
         # make a blank image for the text, initialized to transparent text color
                           
         txt=Image.new('RGBA', base.size, (255,255,255,0))
         (width1, height1) = base.size
         (width2, height2) = txt.size
         # get a font
         fnt = ImageFont.truetype('C:\\path\\to\\a\\font\\Raleway-Medium.ttf', 15)
         # get a drawing context
         d = ImageDraw.Draw(txt)

         # draw text, full opacity
         if url=='http://xkcd.com/111/' or url=='http://xkcd.com/1091/':
             lines = textwrap.wrap(comicTitle, width=60)
         else:
             lines = textwrap.wrap(comicTitle, width=width1/10)
         y=10
         
         for line in lines:
            width, height = fnt.getsize(line)
            d.text((10,y), line, font=fnt, fill=(255,255,255,255))
            y+=height
            

         txt.save(os.path.join('xkcd', os.path.basename(comicUrl[:-3])+'title.png'))  #remove extension with -3
         txt2 = Image.open(os.path.join('xkcd', os.path.basename(comicUrl[:-3])+'title.png'))

         resultWidth = width1
         resultHeight = height1+height2
         
         result = Image.new('RGBA', (resultWidth, resultHeight))
         result.paste(im=base, box=(0, 0))
         result.paste(im=txt2, box=(0,height1))

         result.save(os.path.join('xkcd', os.path.basename(comicUrl[:-3])+'combined.png'))
         #-------------------------
        
    #Get the Prev button's url.
    prevLink = soup.select('a[rel="prev"]')[0]
    url = 'http://xkcd.com' + prevLink.get('href')

print("Cleaning up...")
folder = os.path.abspath('C:\\path\\to\\your\\xkcd')
for foldername, subfolders, filenames in os.walk(folder):
    for filename in filenames:
        if not (filename.endswith('combined.png') or filename.endswith('lyrics.png')):
            os.unlink(folder+'\\'+filename)
                

print('Done.')
