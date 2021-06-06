from urllib import request
url = "https://www.youtube.com/watch?v=fE_spqJTU6k"
html = request.urlopen(url).read().decode('utf8')
html[:60]

from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
title = soup.find('title')

finalTitle = title.string.replace(" - YouTube", "")

print(f"'{finalTitle}'")