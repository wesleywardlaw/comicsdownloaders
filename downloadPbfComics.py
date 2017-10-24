#! python3
# downloadPbfComics.py - Downloads every pbf comic

import requests, os, bs4


url = 'http://www.pbfcomics.com'              # starting url
os.makedirs('pbf', exist_ok=True)  # store comics in ./pbf

while not url.endswith('new-herald-galactus/'):
    # Download the page.
    print('Downloading page %s...' % url)
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text)
    # Find the URL of the comic image.
    comicElem = soup.select('#comic img')
    prev = soup.select('span.pbf-nav-previous a')
    prev = prev[0].get('href')
    print(prev)
    

    if comicElem == []:
         print('Could not find comic image.')
    else:
         try:
             comicUrl = comicElem[0].get('src')
             # Download the image.
             print('Downloading image %s...' % (comicUrl))
             res = requests.get(comicUrl)
             res.raise_for_status()
         except requests.exceptions.MissingSchema:
             # skip this comic
             url = prev
             continue

         # Save the image to ./pbf
         imageFile = open(os.path.join('pbf', os.path.basename(comicUrl)), 'wb')
         for chunk in res.iter_content(100000):
             imageFile.write(chunk)
         imageFile.close()

    url = prev
    continue
                

print('Done.')
