# literally just me testing things
# fair warning this is very messy

from newspaper import Article, Config
import requests as r
from bs4 import BeautifulSoup
import time


if __name__ == "__main__":
    link = "https://www.axios.com/2023/05/30/police-brutality-latino-george-floyd"
    working_link = "https://www.pewresearch.org/short-reads/2023/08/16/11-facts-about-hispanic-origin-groups-in-the-us/"
    link2 = "https://news.google.com/articles/CBMimgFodHRwczovL3d3dy53c2ouY29tL2FydGljbGVzL2hpc3Bhbmljcy1saWtlLXdoYXQtdGhlLWdvcC1pcy1zZWxsaW5nLWNlbnN1cy1taWRkbGUtY2xhc3MtbGFib3ItZm9yY2UtdGF4LXRyYW5zZmVyLXBheW1lbnQtaW5jb21lLWVxdWFsaXR5LXRleGFzLTExNjY2MTk5NjEx0gEA?hl=en-US&gl=US&ceid=US%3Aen"
    results = r.get(link)
    soup = BeautifulSoup(results.text, 'html.parser')
    words = soup.findAll('p')
    news = ""
    for line in words:
        news += line.get_text()
    print(news)
    # with open('news/article' + str(links.index(link)) + '.txt', 'a') as f:
    #     for line in words:
    #         f.write(line.get_text())
    # f.close()
    # article = ""
    # with open('news/article' + str(links.index(link)) + '.txt', 'r') as f:
    #     article = f.read()
    # f.close()