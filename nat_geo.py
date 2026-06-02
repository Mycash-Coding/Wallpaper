wimport os
import ctypes
import urllib.request
import re
from bs4 import BeautifulSoup

# The live NatGeo Photo of the Day page
url = "https://www.nationalgeographic.com/photo-of-the-day"

# Web browsers use a 'User-Agent' header so websites know a human is visiting.
# We include this so NatGeo doesn't block the automated request.
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

try:
    # Request the page
    req = urllib.request.Request(url, headers=headers)
    html = urllib.request.urlopen(req).read()
    
    # Parse the webpage content
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find image URLs embedded in the page metadata or image tags
    img_url = None
    
    # Strategy 1: Look for the primary high-res meta image tag
    meta_tag = soup.find('meta', property='og:image')
    if meta_tag:
        img_url = meta_tag.get('content')
        
    # Strategy 2: Fallback to searching the article body images if metadata changes
    if not img_url:
        for img in soup.find_all('img'):
            src = img.get('src', '')
            if 'background' in src or 'photo-of-the-day' in src:
                img_url = src
                break

    if img_url:
        # Define save path (Your Windows Pictures folder)
        img_dir = os.path.join(os.environ['USERPROFILE'], 'Pictures')
        img_path = os.path.join(img_dir, 'natgeo_daily.jpg')
        
        # Download and save the image
        img_req = urllib.request.Request(img_url, headers=headers)
        with urllib.request.urlopen(img_req) as response, open(img_path, 'wb') as out_file:
            out_file.write(response.read())
        
        # Windows API call to instantly refresh and set the wallpaper
        ctypes.windll.user32.SystemParametersInfoW(20, 0, img_path, 3)
        print("Success! Wallpaper updated with today's National Geographic image.")
    else:
        print("Could not find the daily image link on the page.")
        
except Exception as e:
    print(f"Error: {e}")
