#! python3
# downloadQuestionableContent.py - Downloads every questionablecontent comic

import requests, os, bs4


url = 'http://questionablecontent.net/view.php?comic=1'              # starting url
os.makedirs('qc', exist_ok=True)  # store comics in ./qc

# Download the page.
print('Downloading page %s...' % url)
res = requests.get(url)
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text)
# Find the URL of the comic image.
latest = soup.select('#comicnav li a')

latest = latest[3].get('href')
url='http://www.questionablecontent.net/'+latest

while not url.endswith('#'):
    # Download the page.
    print('Downloading page %s...' % url)
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text)
    # Find the URL of the comic image.
    comicElem = soup.select('#strip')
    prev = soup.select('#comicnav li a')
    prev = prev[1].get('href')
    

    if comicElem == []:
         print('Could not find comic image.')
    else:
         try:
             comicUrl = 'http://www.questionablecontent.net/' + comicElem[0].get('src')[2:]
             # Download the image.
             print('Downloading image %s...' % (comicUrl))
             res = requests.get(comicUrl)
             res.raise_for_status()
         except requests.exceptions.MissingSchema:
             # skip this comic
             url = 'http://www.questionablecontent.net/' + prev
             continue

         # Save the image to ./qc
         imageFile = open(os.path.join('qc', os.path.basename(comicUrl)), 'wb')
         for chunk in res.iter_content(100000):
             imageFile.write(chunk)
         imageFile.close()

    url = 'http://www.questionablecontent.net/' + prev
    continue
                

print('Done.')
