import requests
from bs4 import BeautifulSoup
import urllib.parse

url = input("Insert url: ")
path_for_images = input("Insert Path for images that will be downloaded: ")
response = requests.get(url)

parse = BeautifulSoup(response.text)

# Get all image tags
image_tags = parse.find_all('img')

# Get urls to the images
images = [ url.get('src') for url in image_tags]
# If no images found in the page
if not images:
    sys.exit("No Images on %s" % url)

# Convert int relative urls 
images = [urlparse.urljoin(response.url, url) for url in images]
print '%s images' % len(images)
# Download images to downloaded folder
for url in images:
    r = requests.get(url)
    f = open('%s/%s' path_for_images % url.split('/')[-1], 'w')
    f.write(r.content)
    f.close()
print '[->] Download successful'
