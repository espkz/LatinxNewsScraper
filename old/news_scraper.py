import requests as r
from bs4 import BeautifulSoup
import time, os, ssl, spacy, re
from collections import Counter


# check if number of titles and links is equal
# not sure if title is needed if we're just collecting data
def downloadNews(key):
    global keywords
    gnresults = r.get('https://news.google.com/search?q=' + key + '%20when%3A1y&hl=en-US&gl=US&ceid=US%3Aen')
    soup = BeautifulSoup(gnresults.text, 'html.parser')
    articles = soup.select('article .DY5T1d.RZIKme')
    # titles = [t.text for t in articles]
    links = []
    base_url = 'https://news.google.com'
    for i in soup.select('article .DY5T1d.RZIKme'):
        ss = base_url + i.get('href')[1:]
        links.append(ss)
    for link in links:
        print("On article number " + str(links.index(link)))
        # download article
        try:
            news = r.get(link)
        except:
            print("Cannot get link, skipping " + link + ", index number " + str(links.index(link)))
            continue
        newssoup = BeautifulSoup(news.text, 'html.parser')
        words = newssoup.findAll('p')
        with open('news/article' + str(links.index(link)) + '.txt', 'a') as f:
            for line in words:
                f.write(line.get_text())
        f.close()
        article = ""
        with open('news/article' + str(links.index(link)) + '.txt', 'r') as f:
            article = f.read()
        f.close()
        # os.remove('news/article.txt')
        # strip punctuation and white space and things
        article = re.sub(r'[^\w\s]','', article)
        new_article = " ".join(article.split())
        print(new_article)
        extractData(new_article.lower())

    top_keywords = Counter(keywords).most_common(10)

    print(top_keywords)

def extractData(article):
    global keywords
    nlp = spacy.load("en_core_web_sm")
    tag = ['PROPN', 'ADJ', 'NOUN']
    data = nlp(article)
    for token in data:
        if (token.text in nlp.Defaults.stop_words):
            continue
        if token.pos_ in tag:
            keywords.append(token.text)
    # top_keywords = Counter(words).most_common(10)

    # print(top_keywords)


def main():
    """
    main function for iterating through keywords and downloading related news
    """
    keywords = ["hispanics", "latinos", "latinas", "latinx", "chicanos", "mexican americans", "puerto rican", "cubans"]
    downloadNews(keywords[0])


if __name__ == "__main__":
    # try:
    #     _create_unverified_https_context = ssl._create_unverified_context
    # except AttributeError:
    #     pass
    # else:
    #     ssl._create_default_https_context = _create_unverified_https_context
    #
    # nltk.download('stopwords')
    # nltk.download('punkt')
    keywords = []
    main()