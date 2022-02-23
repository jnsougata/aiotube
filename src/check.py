import re
import aiotube
from urllib.parse import unquote

vid = aiotube.Video('FlUMx2Hnug8')

src = vid.streams

urls = re.findall(r'https://rr(.*?)"', src)
modified = [url.encode().decode('unicode_escape') for url in urls]
actual = list(set([unquote(f"https://rr{url}") for url in modified]))
for url in actual:
    if 'initplayback' not in url:
        print(url)
